#!/usr/bin/env node

/**
 * Rotate image using cli-anything-imutils
 * Usage: node rotate.js --input photo.jpg --output rotated.jpg --angle 90
 */

const { execSync } = require('child_process');
const path = require('path');

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
    const output = args.output || input.replace('.', '_rotated.');
    const angle = args.angle || '0';
    const scale = args.scale || '1.0';
    
    if (!input) {
        console.error('Error: --input is required');
        console.error('Usage: node rotate.js --input photo.jpg --output rotated.jpg --angle 90');
        process.exit(1);
    }
    
    try {
        console.log(`🔄 Rotating image: ${input}`);
        console.log(`   Angle: ${angle}°, Scale: ${scale}`);
        
        const cmd = `cli-anything-imutils rotate-cmd "${input}" "${output}" --angle ${angle} --scale ${scale}`;
        const result = execSync(cmd, { encoding: 'utf-8' });
        
        console.log(`✅ Success: ${output}`);
        console.log(result);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

main();
