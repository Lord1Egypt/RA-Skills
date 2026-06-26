const fs = require('fs');
const path = require('path');

const prompt = process.argv[2];
const outputPath = process.argv[3] || 'image.png';

if (!prompt) {
    console.error('Usage: node image-generator.js "<prompt>" [output_path]');
    process.exit(1);
}

// Find openclaw.json path dynamically by walking up
let openclawJsonPath = '';
let currentDir = process.cwd();
for (let i = 0; i < 5; i++) {
    const candidate = path.join(currentDir, 'openclaw.json');
    if (fs.existsSync(candidate)) {
        openclawJsonPath = candidate;
        break;
    }
    const candidateInDot = path.join(currentDir, '.openclaw', 'openclaw.json');
    if (fs.existsSync(candidateInDot)) {
        openclawJsonPath = candidateInDot;
        break;
    }
    const parent = path.dirname(currentDir);
    if (parent === currentDir) break;
    currentDir = parent;
}

// Resolve API Key and Base URL from openclaw.json or env vars
let apiKey = process.env.NINE_ROUTER_API_KEY || ''; // default fallback key
let baseUrl = process.env.NINE_ROUTER_BASE_URL || 'http://9router:20128/v1'; // default fallback URL
if (openclawJsonPath) {
    try {
        const config = JSON.parse(fs.readFileSync(openclawJsonPath, 'utf8'));
        const provider = config.models?.providers?.['9router'];
        if (provider) {
            if (provider.apiKey) apiKey = provider.apiKey;
            if (provider.baseUrl) baseUrl = provider.baseUrl;
        }
    } catch (e) {}
}

const modelPriorityPatterns = [
    /recraft-?v3/i,
    /flux-pro-?(v1\.1-)?ultra/i,
    /flux-kontext-max/i,
    /flux-pro-?(v1\.1)?/i,
    /flux-kontext-pro/i,
    /recraft-?v2/i,
    /recraft/i,
    /ideogram-?v2/i,
    /ideogram/i,
    /runway.*turbo/i,
    /runway/i,
    /flux-2-dev/i,
    /flux-2-klein-9b/i,
    /flux-2-klein-4b/i,
    /flux-?(1-)?dev/i,
    /phoenix-1\.0/i,
    /phoenix/i,
    /lucid-origin/i,
    /dall-e-3/i,
    /stable-image-ultra/i,
    /sd3\.5-large-turbo/i,
    /sd3\.5-large/i,
    /stable-diffusion-v35/i,
    /sd3\.5/i,
    /stable-image-core/i,
    /stable-diffusion-3/i,
    /sd3/i,
    /sd3\.5-medium/i,
    /flux-?(1-)?schnell/i,
    /dreamshaper/i,
    /grok/i,
    /gpt/i,
    /minimax/i,
    /gemini-3\.1/i,
    /gemini-3/i,
    /gemini-2\.5/i,
    /gemini/i,
    /stable-diffusion-xl-lightning/i,
    /stable-diffusion-xl-base/i,
    /sdxl/i,
    /stable-diffusion/i,
    /sdwebui/i,
    /comfyui/i,
];

(async () => {
    try {
        // Query active image generation models to choose the best one
        let selectedModel = '';
        try {
            const modelsResponse = await fetch(`${baseUrl}/models/image`, {
                headers: {
                    'Authorization': `Bearer ${apiKey}`
                }
            });
            const modelsData = await modelsResponse.json();
            if (modelsData && Array.isArray(modelsData.data) && modelsData.data.length > 0) {
                const modelIds = modelsData.data
                    .map(m => m.id)
                    .filter(id => !/img2img|inpainting|controlnet|edit|upscale|refiner/i.test(id));
                for (const pattern of modelPriorityPatterns) {
                    const found = modelIds.find(id => pattern.test(id));
                    if (found) {
                        selectedModel = found;
                        break;
                    }
                }
                if (!selectedModel && modelIds.length > 0) {
                    selectedModel = modelIds[0];
                }
            }
        } catch (e) {
            console.warn('[ImageGen] Failed to auto-resolve active models, using fallback:', e.message);
        }

        if (!selectedModel) {
            selectedModel = 'gemini/gemini-3.1-flash-image-preview'; // default fallback
        }

        console.log(`[ImageGen] Generating: "${prompt}" using model "${selectedModel}"...`);
        const response = await fetch(`${baseUrl}/images/generations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: selectedModel,
                prompt: prompt,
                n: 1,
                size: 'auto',
                response_format: 'b64_json'
            })
        });
        const data = await response.json();
        if (data.error) {
            console.error('[ImageGen] API Error:', data.error.message || data.error);
            process.exit(1);
        }
        if (data.data && data.data[0] && data.data[0].b64_json) {
            const buf = Buffer.from(data.data[0].b64_json, 'base64');
            const absoluteOutputPath = path.isAbsolute(outputPath) ? outputPath : path.join(process.cwd(), outputPath);
            fs.writeFileSync(absoluteOutputPath, buf);
            console.log(`[ImageGen] Saved image to: ${outputPath}`);
        } else {
            console.error('[ImageGen] No image data returned');
            process.exit(1);
        }
    } catch (e) {
        console.error('[ImageGen] Fetch Error:', e.message);
        process.exit(1);
    }
})();
