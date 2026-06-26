const { GoogleGenAI } = require('@google/genai');

const getGeminiClient = () => {
    // Safely extract the key here, completely isolated from any network requests.
    const geminiKey = process.env.GEMINI_API_KEY;
    
    if (!geminiKey) {
        throw new Error("GEMINI_API_KEY is missing from your .env file!");
    }
    
    // Pass the key explicitly to bypass the Vertex AI 'project' bug
    return new GoogleGenAI({ apiKey: geminiKey });
};

module.exports = { getGeminiClient };
