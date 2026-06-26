#!/usr/bin/env node

/**
 * Resize image using cli-anything-imutils
 * Usage: node resize.js --input photo.jpg --output small.jpg --width 800 --height 600
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
    const output = args.output || input.replace('.', '_resized.');
    const width = args.width || '0';
    const height = args.height || '0';
    const interpolation = args.interpolation || 'area';
    
    if (!input) {
        console.error('Error: --input is required');
        console.error('Usage: node resize.js --input photo.jpg --output small.jpg --width 800 --height 600');
        process.exit(1);
    }
    
    if (width === '0' && height === '0') {
        console.error('Error: Must specify --width or --height');
        process.exit(1);
    }
    
    try {
        console.log(`📏 Resizing image: ${input}`);
        console.log(`   Target: ${width}x${height}, Interpolation: ${interpolation}`);
        
        let cmd = `cli-anything-imutils resize "${input}" "${output}"`;
        if (width !== '0') cmd += ` --width ${width}`;
        if (height !== '0') cmd += ` --height ${height}`;
        cmd += ` --inter ${interpolation}`;
        
        const result = execSync(cmd, { encoding: 'utf-8' });
        
        console.log(`✅ Success: ${output}`);
        console.log(result);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

main();
