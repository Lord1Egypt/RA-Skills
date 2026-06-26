#!/usr/bin/env node

/**
 * Skeletonize image using cli-anything-imutils
 * Usage: node skeleton.js --input photo.jpg --output skeleton.jpg
 */

const { execSync } = require('child_process');

function parseArgs(args) {
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].slice(2);
            const value = args[i + 1];
            parsed[key] = value;
            i++;
        }
    }
    return parsed;
}

function main() {
    const args = parseArgs(process.argv.slice(2));
    
    const input = args.input;
    const output = args.output || input.replace('.', '_skeleton.');
    
    if (!input) {
        console.error('Error: --input is required');
        console.error('Usage: node skeleton.js --input photo.jpg --output skeleton.jpg');
        process.exit(1);
    }
    
    try {
        console.log(`🦴 Skeletonizing image: ${input}`);
        
        const cmd = `cli-anything-imutils skeleton "${input}" "${output}"`;
        const result = execSync(cmd, { encoding: 'utf-8' });
        
        console.log(`✅ Success: ${output}`);
        console.log(result);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

main();
