#!/usr/bin/env node
/**
 * markdown2doc
 * Convert Markdown files to PDF or Word documents
 * Default output directory is the same directory as the source file
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { URL } = require('url');
const crypto = require('crypto');

class Markdown2Doc {
    constructor() {
        // Base URL for conversion service
        this.BASE_URL = "https://lab.hjcloud.com/llmdoc";
    }

    /**
     * Send HTTP request
     * @param {string} url
     * @param {object} options
     * @returns {Promise<{status: number, data: any}>}
     */
    async request(url, options = {}) {
        return new Promise((resolve, reject) => {
            const urlObj = new URL(url);
            const isHttps = urlObj.protocol === 'https:';
            const httpModule = isHttps ? https : http;

            const reqOptions = {
                hostname: urlObj.hostname,
                port: urlObj.port || (isHttps ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: options.method || 'POST',
                headers: options.headers || {},
                timeout: options.timeout || 60000
            };

            const req = httpModule.request(reqOptions, (res) => {
                const chunks = [];

                res.on('data', (chunk) => {
                    chunks.push(chunk);
                });

                res.on('end', () => {
                    const buffer = Buffer.concat(chunks);
                    let data;

                    if (options.responseType === 'arraybuffer') {
                        data = buffer;
                    } else {
                        const text = buffer.toString('utf8');
                        try {
                            data = JSON.parse(text);
                        } catch (e) {
                            data = text;
                        }
                    }

                    resolve({
                        status: res.statusCode,
                        headers: res.headers,
                        data: data
                    });
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });

            if (options.body) {
                req.write(options.body);
            }

            req.end();
        });
    }

    /**
     * Check path traversal
     * Only allow files inside markdown directory
     */
    isPathSafe(baseDir, targetPath) {
        try {
            const resolvedBase = path.resolve(baseDir);
            const resolvedTarget = path.resolve(targetPath);

            // 防止 /dir1 和 /dir11 误判
            const baseWithSep = resolvedBase.endsWith(path.sep)
                ? resolvedBase
                : resolvedBase + path.sep;

            return resolvedTarget.startsWith(baseWithSep);

        } catch (e) {
            return false;
        }
    }

    /**
     * Extract image references from markdown content
     * @param {string} mdContent - Markdown content
     * @returns {Array<{fullSyntax: string, alt: string, path: string, isLocal: boolean}>}
     */
    extractImages(mdContent) {
        const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
        const images = [];
        let match;

        while ((match = imageRegex.exec(mdContent)) !== null) {
            const fullSyntax = match[0];
            const alt = match[1];
            const imgPath = match[2];

            // Skip URLs and base64 images
            const isLocal = !imgPath.startsWith('http://') &&
                           !imgPath.startsWith('https://') &&
                           !imgPath.startsWith('data:');

            images.push({
                fullSyntax: fullSyntax,
                alt: alt,
                path: imgPath,
                isLocal: isLocal
            });
        }

        return images;
    }

    /**
     * Get MIME type from filename
     * @param {string} filename
     * @returns {string}
     */
    getContentType(filename) {
        const ext = path.extname(filename).toLowerCase();
        const mimeTypes = {
            '.md': 'text/plain',
            '.markdown': 'text/markdown',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml'
        };
        return mimeTypes[ext] || 'application/octet-stream';
    }

    /**
     * Build multipart form data for file upload
     * @param {Object} fields - Key-value pairs for form fields (non-file data)
     * @param {Array<{name: string, data: Buffer, filename: string}>} files - Files to upload
     * @returns {{boundary: string, body: Buffer}}
     */
    buildMultipartFormData(fields, files) {
        const boundary = '----FormBoundary' + crypto.randomBytes(16).toString('hex');
        const parts = [];

        // Add fields
        for (const [name, value] of Object.entries(fields)) {
            if (value !== null && value !== undefined) {
                parts.push(Buffer.from(
                    `--${boundary}\r\n` +
                    `Content-Disposition: form-data; name="${name}"\r\n\r\n` +
                    `${value}\r\n`
                ));
            }
        }

        // Add files
        for (const file of files) {
            const contentType = file.contentType || this.getContentType(file.filename);
            const header = Buffer.from(
                `--${boundary}\r\n` +
                `Content-Disposition: form-data; name="${file.name}"; filename="${file.filename}"\r\n` +
                `Content-Type: ${contentType}\r\n\r\n`
            );
            const footer = Buffer.from('\r\n');
            parts.push(Buffer.concat([header, file.data, footer]));
        }

        parts.push(Buffer.from(`--${boundary}--\r\n`));
        return {
            boundary: boundary,
            body: Buffer.concat(parts)
        };
    }

    /**
     * List available themes
     * @returns {Promise<void>}
     */
    async listThemes() {
        const fullUrl = this.BASE_URL + '/v1/skills/public/markdown2doc/themes';
        try {
            const response = await this.request(fullUrl, { method: 'GET' });
            if (response.status !== 200) {
                console.log(`Failed to fetch themes, status code: ${response.status}`);
                return;
            }
            const data = response.data;
            const themes = Array.isArray(data) ? data : (data.themes || []);
            if (Array.isArray(themes) && themes.length > 0) {
                console.log('Available themes:');
                themes.forEach(t => {
                    const name = t.theme || t;
                    const formats = t.formats && t.formats.length > 0 ? ` [${t.formats.join(', ')}]` : '';
                    const desc = t.desc ? `  - ${t.desc}` : '';
                    console.log(`  ${name}${formats}${desc}`);
                });
            } else {
                console.log('No themes available.');
            }
        } catch (error) {
            console.log(`Error fetching themes: ${error.message}`);
        }
    }

    /**
     * Convert markdown file to PDF or Word
     * @param {string} filePath - Path to the markdown file
     * @param {string} outputType - Output format: 'pdf' or 'docx' (default: 'pdf')
     * @param {string|null} theme - Theme name for docx output (optional)
     * @returns {Promise<string|null>} - Path to the converted file, or null on failure
     */
    async convertFile(filePath, outputType = 'pdf', theme = null) {
        // 1. Validate input file
        if (!fs.existsSync(filePath)) {
            console.log(`Error: File does not exist - ${filePath}`);
            return null;
        }

        const resolvedPath = path.resolve(filePath);
        const markdownContent = fs.readFileSync(resolvedPath, 'utf8');

        if (!markdownContent || markdownContent.trim() === '') {
            console.log(`Error: Markdown file is empty - ${filePath}`);
            return null;
        }

        console.log(`[1/2] Converting markdown to ${outputType.toUpperCase()}: ${filePath}`);

        try {
            // 2. Extract local images from markdown
            const images = this.extractImages(markdownContent);
            const localImages = images.filter(img => img.isLocal);
            const mdFileDir = path.dirname(resolvedPath);

            // Build image mapping and file list
            const imageMapping = {};
            const filesToUpload = [];
            let imageIndex = 0;

            for (const img of localImages) {
                // Resolve image path relative to markdown file
                let imgAbsPath;
                if (path.isAbsolute(img.path)) {
                    imgAbsPath = img.path;
                } else {
                    imgAbsPath = path.resolve(mdFileDir, img.path);
                }

                // SECURITY: prevent path traversal
                if (!this.isPathSafe(mdFileDir, imgAbsPath)) {
                    console.log(`  Security warning: Path traversal blocked: ${imgAbsPath}`);
                    continue;
                }

                if (fs.existsSync(imgAbsPath)) {
                    const imgBuffer = fs.readFileSync(imgAbsPath);
                    const imgFilename = path.basename(img.path);

                    // Use index in field name for multiple images
                    imageMapping[img.fullSyntax] = imageIndex;
                    filesToUpload.push({
                        name: `md_file`,
                        data: imgBuffer,
                        filename: imgFilename
                    });

                    console.log(`  Found local image: ${img.path} (index: ${imageIndex})`);
                    imageIndex++;
                } else {
                    console.log(`  Warning: Local image not found: ${imgAbsPath}`);
                }
            }

            // 3. Select endpoint based on output type
            const endpoint = outputType === 'docx'
                ? '/v1/skills/public/markdown2doc/docx'
                : '/v1/skills/public/markdown2doc/pdf';
            const fullUrl = this.BASE_URL + endpoint;

            // 4. Build multipart form data
            const fields = {};
            if (Object.keys(imageMapping).length > 0) {
                fields.image_mapping = JSON.stringify(imageMapping);
            }
            if (theme) {
                fields.theme = theme;
            }

            // Add md_file as the first file
            const allFiles = [
                {
                    name: 'md_file',
                    data: Buffer.from(markdownContent, 'utf8'),
                    filename: path.basename(resolvedPath),
                    contentType: 'text/markdown'
                },
                ...filesToUpload
            ];

            // Build multipart body
            const { boundary, body: multipartBody } = this.buildMultipartFormData(fields, allFiles);

            // 5. Send request to conversion service
            const response = await this.request(fullUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${boundary}`,
                    'Content-Length': multipartBody.length
                },
                body: multipartBody,
                timeout: 120000,
                responseType: 'arraybuffer'
            });

            if (response.status !== 200) {
                console.log(`Conversion failed, status code: ${response.status}`);
                const errText = Buffer.isBuffer(response.data)
                    ? response.data.toString('utf8')
                    : String(response.data);
                console.log(`Error message: ${errText}`);
                return null;
            }

            // Status 200 may still carry a JSON error body
            const rawText = Buffer.isBuffer(response.data)
                ? response.data.toString('utf8')
                : String(response.data);
            try {
                const json = JSON.parse(rawText);
                if (json.success === false) {
                    console.log(`API request failed: ${json.err || 'Unknown error'}`);
                    return null;
                }
            } catch (e) {
                // Not JSON — binary file response, treat as success
            }

            // 6. Save the converted file
            const parentDir = path.dirname(resolvedPath);
            let outputFileName;
            const disposition = response.headers['content-disposition'];
            if (disposition) {
                // filename*=UTF-8''xxx.pdf 或 filename="xxx.pdf"
                const utf8Match = disposition.match(/filename\*=UTF-8''([^;\s]+)/i);
                const asciiMatch = disposition.match(/filename="?([^";\s]+)"?/i);
                const raw = utf8Match ? decodeURIComponent(utf8Match[1]) : (asciiMatch ? asciiMatch[1] : null);
                if (raw) outputFileName = raw;
            }
            if (!outputFileName) {
                outputFileName = `${path.parse(resolvedPath).name}.${outputType}`;
            }
            const outPath = path.join(parentDir, outputFileName);

            if (Buffer.isBuffer(response.data)) {
                fs.writeFileSync(outPath, response.data);
            } else {
                console.log(`Error: Expected file stream but got ${typeof response.data}`);
                return null;
            }

            console.log(`[2/2] Conversion complete, file saved: ${outPath}`);
            return outPath;

        } catch (error) {
            console.log(`Error occurred during conversion: ${error.message}`);
            return null;
        }
    }
}

const USAGE = `Usage:
  node markdown2doc.js convert <file_path> [format] [--theme <name>]   Convert markdown file to PDF or DOCX
  node markdown2doc.js list-themes                                      List available themes

Examples:
  node markdown2doc.js convert readme.md pdf
  node markdown2doc.js convert readme.md docx
  node markdown2doc.js convert readme.md docx --theme dark
  node markdown2doc.js list-themes`;

async function main() {
    if (process.argv.length < 3) {
        console.log(USAGE);
        process.exit(1);
    }

    const converter = new Markdown2Doc();
    const cmd = process.argv[2];

    if (cmd === "list-themes") {
        await converter.listThemes();

    } else if (cmd === "convert") {
        if (process.argv.length < 4) {
            console.log("Usage: node markdown2doc.js convert <file_path> [format] [--theme <name>]");
            console.log("  format: 'pdf' (default) or 'docx'");
            process.exit(1);
        }

        const filePath = process.argv[3];
        let outputType = 'pdf';
        let theme = null;

        const remainingArgs = process.argv.slice(4);
        const themeIdx = remainingArgs.indexOf('--theme');
        if (themeIdx !== -1) {
            theme = remainingArgs[themeIdx + 1] || null;
            remainingArgs.splice(themeIdx, 2);
        }

        if (remainingArgs.length > 0) {
            const formatArg = remainingArgs[0].toLowerCase();
            if (formatArg === 'pdf' || formatArg === 'docx') {
                outputType = formatArg;
            } else {
                console.log(`Unknown format: ${formatArg}`);
                console.log("Supported formats: pdf, docx");
                process.exit(1);
            }
        }

        const result = await converter.convertFile(filePath, outputType, theme);
        if (!result) {
            process.exit(1);
        }

    } else {
        // Backward compatibility: treat direct file path as convert
        if (fs.existsSync(cmd) && fs.statSync(cmd).isFile()) {
            const outputType = process.argv.length >= 4 ? process.argv[3] : 'pdf';
            const result = await converter.convertFile(cmd, outputType);
            if (!result) {
                process.exit(1);
            }
        } else {
            console.log(`Unknown command or file not found: ${cmd}`);
            console.log(USAGE);
            process.exit(1);
        }
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error(`Program execution error: ${error.message}`);
        process.exit(1);
    });
}

module.exports = Markdown2Doc;