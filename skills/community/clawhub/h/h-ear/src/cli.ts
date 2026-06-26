#!/usr/bin/env node
/**
 * h-ear CLI — manifest-driven dispatcher for the H-ear OpenClaw skill.
 *
 * The command surface (commands, flags, positionals, descriptions, examples)
 * is declared exactly once in [manifest.ts]. This file only:
 *   1. Parses argv into { positionals, flags, bools }
 *   2. Resolves the manifest entry for the user's path
 *   3. Calls its handler, prints the formatted result
 *   4. Emits help (top-level, per-subcommand) and `--list-tools --json` from
 *      the same manifest
 *
 * If a flag is missing or wrong, the LLM (or human) sees a "did you mean"
 * pointer at the next-likely subcommand instead of a stack trace.
 */

import { readFileSync, unlinkSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { spawnSync } from 'child_process';
import { join } from 'path';
import { tmpdir } from 'os';
import { toolDescriptions, toolShapes } from '@h-ear/core';
import { createSkill } from './index.js';
import { COMMANDS, findCommand, listToolsJson, type CommandSpec, type ParsedArgs } from './manifest.js';
import { classifyFileCommand } from './commands/classify.js';

// ─── Argv parser ─────────────────────────────────────────────────────────────

interface ParseResult {
    pathTokens: string[];
    parsed: ParsedArgs;
    wantsHelp: boolean;
}

/** Split argv into path tokens + flag/positional buckets. */
function parseArgv(argv: string[], spec: CommandSpec | null): ParseResult {
    const flags: Record<string, string | undefined> = {};
    const bools: Record<string, boolean> = {};
    const positionalValues: string[] = [];
    let wantsHelp = false;

    // First, pull out the path tokens for the matched spec — they are NOT positionals.
    const pathLen = spec?.cliPath.length ?? 0;
    const rest = argv.slice(pathLen);

    for (let i = 0; i < rest.length; i++) {
        const tok = rest[i];
        if (tok === '--help' || tok === '-h') { wantsHelp = true; continue; }
        if (tok.startsWith('--')) {
            const name = tok.slice(2);
            const next = rest[i + 1];
            if (next !== undefined && !next.startsWith('-')) {
                flags[name] = next;
                i++;
            } else {
                bools[name] = true;
            }
        } else {
            positionalValues.push(tok);
        }
    }

    // Bind positional values to their declared names in spec order.
    const positionals: Record<string, string | undefined> = {};
    if (spec?.positionals) {
        spec.positionals.forEach((p, idx) => {
            positionals[p.name] = positionalValues[idx];
        });
    }

    return {
        pathTokens: argv.slice(0, pathLen),
        parsed: { positionals, flags, bools },
        wantsHelp,
    };
}

// ─── Help renderers ──────────────────────────────────────────────────────────

const HEADER = `h-ear — Sound Intelligence CLI for the H-ear API
Documentation: https://h-ear.world  ·  Skill: @h-ear/openclaw

Usage:
  h-ear <command> [args] [flags]
  h-ear <command> --help            Show flags + examples for one command
  h-ear --list-tools --json         Emit MCP-style schemas for all commands
  h-ear --version                   Print the skill version`;

const ENV_DOCS = `Environment variables:
  HEAR_API_KEY      H-ear Enterprise API key (required for most commands)
  HEAR_BEARER_TOKEN OAuth bearer (alternative to HEAR_API_KEY)
  HEAR_ENV          dev | staging | prod (default: prod)
  HEAR_BASE_URL     Override base URL (advanced)
  LISTEN_RTSP_URL   RTSP source (only for h-ear capture)`;

function pad(s: string, n: number): string { return s.length >= n ? s : s + ' '.repeat(n - s.length); }

function renderTopLevelHelp(): string {
    const lines: string[] = [HEADER, '', 'Commands:'];

    // Group by first path token so multi-level commands cluster nicely.
    const groups = new Map<string, CommandSpec[]>();
    for (const spec of COMMANDS) {
        const head = spec.cliPath[0];
        const existing = groups.get(head);
        if (existing) existing.push(spec);
        else groups.set(head, [spec]);
    }
    // Stable group order: alphabetical.
    const groupNames = [...groups.keys()].sort();

    for (const name of groupNames) {
        const specs = groups.get(name) ?? [];
        for (const spec of specs) {
            const path = spec.cliPath.join(' ');
            const positionalStr = spec.positionals?.map(p => `<${p.name}>`).join(' ') ?? '';
            const sig = `${path}${positionalStr ? ' ' + positionalStr : ''}`;
            lines.push(`  ${pad(sig, 32)}${spec.summary}`);
        }
    }

    lines.push('', ENV_DOCS);
    return lines.join('\n');
}

function renderCommandHelp(spec: CommandSpec): string {
    const path = spec.cliPath.join(' ');
    const positionalStr = spec.positionals?.map(p => `<${p.name}>`).join(' ') ?? '';
    const lines: string[] = [
        `h-ear ${path}${positionalStr ? ' ' + positionalStr : ''}`,
        '',
        spec.summary,
        '',
        toolDescriptions[spec.schemaName] ?? '',
        '',
    ];

    if (spec.positionals?.length) {
        lines.push('Positional arguments:');
        for (const p of spec.positionals) {
            const shape = toolShapes[spec.schemaName];
            const zod = shape?.[p.schemaKey];
            const desc = (zod as { _def?: { description?: string } } | undefined)?._def?.description ?? '';
            lines.push(`  ${pad(`<${p.name}>`, 24)}${desc}`);
        }
        lines.push('');
    }

    if (spec.flags?.length) {
        lines.push('Flags:');
        for (const f of spec.flags) {
            const shape = toolShapes[spec.schemaName];
            const zod = shape?.[f.schemaKey];
            const desc = (zod as { _def?: { description?: string } } | undefined)?._def?.description ?? '';
            lines.push(`  ${pad(`--${f.name}`, 24)}${desc}`);
        }
        lines.push('');
    }

    lines.push('Examples:');
    for (const ex of spec.examples) lines.push(`  ${ex}`);
    return lines.join('\n');
}

/**
 * Find the most plausible commands given an unrecognised CLI path.
 * Used to suggest "did you mean..." instead of failing opaquely.
 */
function suggestNear(tokens: string[]): CommandSpec[] {
    if (tokens.length === 0) return [];
    const head = tokens[0];
    return COMMANDS.filter(c => c.cliPath[0] === head).slice(0, 5);
}

// ─── Capture (RTSP audio) — lives in CLI; not in manifest because it does I/O ──

function captureAudio(sourceUrl: string, durationSec: number): { buffer: Buffer; fileName: string } {
    const tmpDir = join(tmpdir(), 'h-ear-listen');
    if (!existsSync(tmpDir)) mkdirSync(tmpDir, { recursive: true });

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').replace('T', '_').slice(0, 19);
    const outFile = join(tmpDir, `capture_${timestamp}_${durationSec}s.wav`);

    const ffmpegArgs: string[] = ['-y'];
    if (sourceUrl.startsWith('rtsp://')) ffmpegArgs.push('-rtsp_transport', 'tcp');
    ffmpegArgs.push(
        '-i', sourceUrl,
        '-vn', '-ac', '1', '-ar', '16000', '-acodec', 'pcm_s16le',
        '-t', String(durationSec), '-f', 'wav', outFile,
    );

    const result = spawnSync('ffmpeg', ffmpegArgs, {
        stdio: ['pipe', 'pipe', 'pipe'],
        encoding: 'utf-8',
        timeout: (durationSec + 30) * 1000,
    });

    if (result.status !== 0 || !existsSync(outFile)) {
        const stderr = (result.stderr || '').trim().split('\n').slice(-3).join('\n');
        throw new Error(`ffmpeg capture failed (exit ${result.status}): ${stderr}`);
    }

    const buffer = readFileSync(outFile);
    try { unlinkSync(outFile); } catch (err) { console.error(`  Cleanup warning: failed to remove temp file ${outFile}`, err); }
    return { buffer: Buffer.from(buffer), fileName: `capture_${timestamp}_${durationSec}s.wav` };
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
    const argv = process.argv.slice(2);

    // Top-level switches that don't need a skill instance:
    if (argv.length === 0 || argv[0] === 'help' || argv[0] === '--help' || argv[0] === '-h') {
        console.log(renderTopLevelHelp());
        return;
    }
    if (argv[0] === '--version' || argv[0] === '-v') {
        const { version } = createSkillSafe();
        console.log(version);
        return;
    }
    if (argv[0] === '--list-tools') {
        if (argv.includes('--json')) {
            console.log(JSON.stringify(listToolsJson(), null, 2));
        } else {
            // Human-readable enumeration for terminal users.
            for (const spec of COMMANDS) {
                console.log(`${spec.cliPath.join(' ').padEnd(28)}${spec.summary}`);
            }
        }
        return;
    }

    // Manifest-driven commands first.
    const matched = findCommand(argv);
    if (matched) {
        const { spec } = matched;
        const parsed = parseArgv(argv, spec);
        if (parsed.wantsHelp) {
            console.log(renderCommandHelp(spec));
            return;
        }
        const { client } = createSkill();
        const out = await spec.handler(client, parsed.parsed);
        console.log(out);
        return;
    }

    // Special-case: capture stays imperative (does ffmpeg I/O before classifying).
    if (argv[0] === 'listen' || argv[0] === 'capture') {
        const parsed = parseArgv(argv, null);
        if (parsed.wantsHelp) {
            console.log([
                'h-ear capture [--rtsp <url>] [--duration 15] [--no-classify]',
                '',
                'Capture audio from an RTSP camera and (by default) classify it.',
                '',
                'Flags:',
                `  ${pad('--rtsp <url>', 24)}RTSP source URL (or set LISTEN_RTSP_URL).`,
                `  ${pad('--duration <sec>', 24)}Capture length in seconds (default 15).`,
                `  ${pad('--no-classify', 24)}Capture only, do not submit for classification.`,
                '',
                'Examples:',
                '  h-ear capture --duration 30',
                '  LISTEN_RTSP_URL=rtsp://cam:554/stream h-ear capture',
            ].join('\n'));
            return;
        }
        const rtspUrl = parsed.parsed.flags.rtsp ?? process.env.LISTEN_RTSP_URL;
        if (!rtspUrl) {
            console.error('Error: RTSP URL required. Pass --rtsp <url> or set LISTEN_RTSP_URL');
            process.exit(1);
        }
        const duration = parseInt(parsed.parsed.flags.duration ?? '15', 10);
        const classifyAfter = !parsed.parsed.bools['no-classify'];

        console.error(`  Capturing ${duration}s audio from ${rtspUrl}...`);
        const { buffer, fileName } = captureAudio(rtspUrl, duration);
        console.error(`  Captured ${(buffer.length / 1024).toFixed(0)} KB`);

        if (classifyAfter) {
            const { client } = createSkill();
            const tmpFile = join(tmpdir(), 'h-ear-listen', fileName);
            writeFileSync(tmpFile, buffer);
            try {
                console.log(await classifyFileCommand(
                    client,
                    tmpFile,
                    { threshold: 0.3, waitForResult: true },
                    (msg) => console.error(`  ${msg}`),
                ));
            } finally {
                try { unlinkSync(tmpFile); } catch { /* best effort */ }
            }
        } else {
            console.log(`Captured: ${fileName} (${(buffer.length / 1024).toFixed(0)} KB)`);
        }
        return;
    }

    // Unknown — give the LLM (or human) a useful pointer instead of a stack trace.
    const suggestions = suggestNear(argv);
    console.error(`Unknown command: ${argv.join(' ')}`);
    if (suggestions.length > 0) {
        console.error('');
        console.error('Did you mean:');
        for (const s of suggestions) {
            console.error(`  h-ear ${s.cliPath.join(' ')}    ${s.summary}`);
        }
    } else {
        console.error('');
        console.error("Run 'h-ear help' or 'h-ear --list-tools' to see all commands.");
    }
    process.exit(1);
}

/** Like createSkill, but tolerant of missing API key (we may just want --version). */
function createSkillSafe(): { version: string } {
    try {
        return createSkill();
    } catch {
        // Resolve version directly from package.json without instantiating the client.
        const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf-8'));
        return { version: pkg.version };
    }
}

main().catch((err: Error) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
});
