// @ts-nocheck
'use strict';

import fs  from 'fs';
import path  from 'path';

function loadIgnoreFile(scanDir) {
    const ignoredSkills = new Set();
    const ignoredPatterns = new Set();
    const ignorePaths = [
        path.join(scanDir, '.guard-scanner-ignore'),
        path.join(scanDir, '.guava-guard-ignore'),
    ];

    for (const ignorePath of ignorePaths) {
        if (!fs.existsSync(ignorePath)) continue;
        const lines = fs.readFileSync(ignorePath, 'utf-8').split('\n');
        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('#')) continue;
            if (trimmed.startsWith('pattern:')) ignoredPatterns.add(trimmed.replace('pattern:', '').trim());
            else ignoredSkills.add(trimmed);
        }
        break;
    }

    return { ignoredSkills, ignoredPatterns };
}

function loadTextFile(filePath, maxLength = 500000) {
    try {
        const content = fs.readFileSync(filePath, 'utf-8');
        if (content.length > maxLength) return null;
        return content;
    } catch {
        return null;
    }
}

export { 
    loadIgnoreFile,
    loadTextFile,
 };
