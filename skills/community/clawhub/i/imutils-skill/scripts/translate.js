#!/usr/bin/env node

/**
 * Translate (shift) image using cli-anything-imutils
 * Usage: node translate.js --input photo.jpg --output shifted.jpg --x 50 --y 30
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
    const output = args.output || input.replace('.', '_shifted.');
    const x = args.x || '0';
    const y = args.y || '0';
    
    if (!input) {
        console.error('Error: --input is required');
        console.error('Usage: node translate.js --input photo.jpg --output shifted.jpg --x 50 --y 30');
        process.exit(1);
    }
    
    try {
        console.log(`↔️  Translating image: ${input}`);
        console.log(`   Shift: X=${x}, Y=${y}`);
        
        const cmd = `cli-anything-imutils translate-cmd "${input}" "${output}" --x ${x} --y ${y}`;
        const result = execSync(cmd, { encoding: 'utf-8' });
        
        console.log(`✅ Success: ${output}`);
        console.log(result);
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

main();
