/**
 * Tests scripts/install-memoria.sh : syntaxe (`sh -n`), garde anti-écrasement
 * (modifications locales → refus du reset --hard), avertissement Node non-LTS.
 * Le script lit MEMORIA_REPO_DIR / MEMORIA_HOME / HOME depuis l'environnement
 * (défauts inchangés pour l'utilisateur) — c'est ce qui le rend testable ici
 * sans toucher au vrai $HOME ni au réseau : la garde sort AVANT npm install.
 */
import { spawnSync } from 'node:child_process'
import { chmodSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'

const SCRIPT = fileURLToPath(new URL('../../../scripts/install-memoria.sh', import.meta.url))

let home: string

/** Lance le script dans un HOME jetable, avec PATH/env surchargés. */
function runScript(env: Record<string, string> = {}, pathPrefix?: string) {
  const path = pathPrefix ? `${pathPrefix}:${process.env['PATH'] ?? ''}` : (process.env['PATH'] ?? '')
  const res = spawnSync('sh', [SCRIPT], {
    env: { HOME: home, PATH: path, ...env },
    encoding: 'utf8',
    timeout: 30_000,
  })
  return { status: res.status, stdout: res.stdout, stderr: res.stderr }
}

/** Dépôt git avec une modification locale stagée (status --porcelain non vide). */
function makeDirtyRepo(): string {
  const repo = join(home, 'openclaw-memoria')
  mkdirSync(repo, { recursive: true })
  const git = (...a: string[]) =>
    spawnSync('git', ['-C', repo, ...a], { env: { ...process.env, HOME: home }, encoding: 'utf8' })
  expect(git('init', '-q').status).toBe(0)
  writeFileSync(join(repo, 'modif-locale.txt'), 'travail en cours\n', 'utf8')
  expect(git('add', 'modif-locale.txt').status).toBe(0)
  return repo
}

beforeEach(() => {
  home = mkdtempSync(join(tmpdir(), 'memoria-install-'))
})

afterEach(() => {
  rmSync(home, { recursive: true, force: true })
})

describe('install-memoria.sh', () => {
  it('syntaxe valide (sh -n)', () => {
    const res = spawnSync('sh', ['-n', SCRIPT], { encoding: 'utf8' })
    expect(res.stderr).toBe('')
    expect(res.status).toBe(0)
  })

  it('garde anti-écrasement : modifications locales → refus + conseil memoria update, exit 1', () => {
    const repo = makeDirtyRepo()
    const { status, stderr } = runScript({ MEMORIA_REPO_DIR: repo })
    expect(status).toBe(1)
    expect(stderr).toContain('Des modifications locales existent')
    expect(stderr).toContain('memoria update')
  })

  it('Node impair (non-LTS) : avertit sans bloquer, recommande Node 22 LTS', () => {
    // Faux `node` v21 en tête de PATH ; le dépôt sale fait sortir le script
    // juste après (garde) — aucun npm install, aucun réseau.
    const fakeBin = join(home, 'fake-bin')
    mkdirSync(fakeBin, { recursive: true })
    const fakeNode = join(fakeBin, 'node')
    writeFileSync(
      fakeNode,
      '#!/bin/sh\ncase "$1" in\n  -v) echo "v21.7.0" ;;\n  -p) case "$2" in *split*) echo 21 ;; *) echo undefined ;; esac ;;\nesac\n',
      'utf8',
    )
    chmodSync(fakeNode, 0o755)
    const repo = makeDirtyRepo()
    const { status, stdout, stderr } = runScript({ MEMORIA_REPO_DIR: repo }, fakeBin)
    expect(stdout).toContain('non-LTS')
    expect(stdout).toContain('Node 22 LTS')
    expect(stdout).toContain('Node v21.7.0 OK') // a continué malgré l'avertissement
    expect(status).toBe(1) // sortie par la garde anti-écrasement, pas par le check Node
    expect(stderr).toContain('Des modifications locales existent')
  })

  it('Node trop vieux (< 20) : erreur bloquante', () => {
    const fakeBin = join(home, 'fake-bin')
    mkdirSync(fakeBin, { recursive: true })
    const fakeNode = join(fakeBin, 'node')
    writeFileSync(
      fakeNode,
      '#!/bin/sh\ncase "$1" in\n  -v) echo "v18.20.0" ;;\n  -p) case "$2" in *split*) echo 18 ;; *) echo undefined ;; esac ;;\nesac\n',
      'utf8',
    )
    chmodSync(fakeNode, 0o755)
    const { status, stderr } = runScript({}, fakeBin)
    expect(status).toBe(1)
    expect(stderr).toContain('requiert Node 20+')
  })
})
