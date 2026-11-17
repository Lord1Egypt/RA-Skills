import assert from 'node:assert/strict'
import { readFile, readdir } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { checkProject, normalizePathSeparators } from '../scripts/check-project.mjs'

const root = dirname(dirname(fileURLToPath(import.meta.url)))
const starter = join(root, 'starter')
const frameworkSource = join(root, 'framework-source')
const version = (await readFile(join(root, 'VERSION'), 'utf8')).trim()
const packageState = JSON.parse(await readFile(join(root, 'package.json'), 'utf8'))
assert.equal(packageState.name, 'multi-screen-wireframe', 'package name is stale')
assert.equal(packageState.version, version, 'VERSION and package.json must match')
assert.equal(version, '2.1.0', 'v2 release version is stale')
assert.equal(
  normalizePathSeparators('framework\\runtime\\board.js'),
  'framework/runtime/board.js',
  'Windows path separators must be normalized before portable suffix checks',
)

const skillSource = await readFile(join(root, 'SKILL.md'), 'utf8')
const frontmatter = skillSource.match(/^---\n([\s\S]*?)\n---/)
assert.ok(frontmatter, 'SKILL.md frontmatter is missing')
const frontmatterKeys = [...frontmatter[1].matchAll(/^([a-z_]+):/gm)].map((match) => match[1]).sort()
assert.deepEqual(frontmatterKeys, ['description', 'name'], 'SKILL.md frontmatter may only contain name and description')
assert.match(frontmatter[1], /^name: multi-screen-wireframe$/m, 'SKILL.md name is stale')
assert.match(skillSource, new RegExp(`multi-screen-wireframe@${version.replaceAll('.', '\\.')}`), 'SKILL.md version example is stale')
assert.match(skillSource, /src\/app\.jsx[\s\S]*v1 React\/JSX/, 'SKILL.md must detect v1 deliverables before editing')
assert.match(skillSource, /不得原地迁移|不得原地覆盖/, 'SKILL.md must prohibit in-place v1 to v2 migration')

const agentSource = await readFile(join(root, 'agents/openai.yaml'), 'utf8')
assert.match(agentSource, /\$multi-screen-wireframe/, 'agents/openai.yaml default prompt must mention the skill')

const rootAgentsSource = await readFile(join(root, 'AGENTS.md'), 'utf8')
const starterAgentsSource = await readFile(join(starter, 'AGENTS.md'), 'utf8')
assert.match(rootAgentsSource, /组件.*改动[\s\S]*同步更新.*COMPONENTS\.md|COMPONENTS\.md[\s\S]*组件.*改动/, 'root AGENTS.md must require component documentation sync')
assert.match(starterAgentsSource, /组件.*改动[\s\S]*同步更新.*COMPONENTS\.md|COMPONENTS\.md[\s\S]*组件.*改动/, 'starter AGENTS.md must require component documentation sync')
assert.match(rootAgentsSource, /v1 \/ v2.*framework|framework.*v1 \/ v2/, 'root AGENTS.md must prohibit cross-major framework upgrades')
assert.match(starterAgentsSource, /v1.*v2.*迁移[\s\S]*新目录|新目录[\s\S]*v1.*v2.*迁移/, 'starter AGENTS.md must require copy-on-migration')

const changelogSource = await readFile(join(root, 'CHANGELOG.md'), 'utf8')
assert.match(changelogSource, /^## 2\.1\.0$/m, 'CHANGELOG.md must document v2.1.0')
assert.match(changelogSource, /^## 2\.0\.0$/m, 'CHANGELOG.md must document v2.0.0')
assert.match(changelogSource, /^## 1\.8\.0$/m, 'CHANGELOG.md must document frozen v1.8.0')

const readmeSource = await readFile(join(root, 'README.md'), 'utf8')
const readmeEnSource = await readFile(join(root, 'README.en.md'), 'utf8')
assert.ok(readmeSource.includes('](README.en.md)'), 'README.md must link to README.en.md for language switch')
assert.ok(readmeEnSource.includes('](README.md)'), 'README.en.md must link to README.md for language switch')
assert.ok(readmeSource.includes('](docs/使用说明.md)'), 'README.md must link to Chinese user guide')
assert.ok(readmeSource.includes('](docs/user-guide.md)'), 'README.md must link to English user guide')
assert.ok(readmeEnSource.includes('](docs/user-guide.md)'), 'README.en.md must link to English user guide')
assert.ok(readmeEnSource.includes('](docs/使用说明.md)'), 'README.en.md must link to Chinese user guide')

const userGuideZh = await readFile(join(root, 'docs/使用说明.md'), 'utf8')
const userGuideEn = await readFile(join(root, 'docs/user-guide.md'), 'utf8')
assert.ok(userGuideZh.includes('](user-guide.md)'), 'docs/使用说明.md must link to English user guide')
assert.ok(userGuideEn.includes('](使用说明.md)'), 'docs/user-guide.md must link to Chinese user guide')

for (const heading of [
  '能做什么',
  '功能示意',
  '不适合',
  '安装',
  '生成新原型',
  '修改交付物',
  '添加与同步注释',
  '快捷键与画板设置',
  '平台与版本',
]) {
  assert.match(readmeSource, new RegExp(`^#{2,3} ${heading}\\s*$`, 'm'), `README.md is missing ${heading}`)
}
for (const heading of [
  'What it does',
  'Screenshots',
  'Not for',
  'Install',
  'Generate a prototype',
  'Edit a deliverable',
  'Annotate and sync',
  'Shortcuts and board settings',
  'Platforms',
]) {
  assert.match(readmeEnSource, new RegExp(`^#{2,3} ${heading}\\s*$`, 'm'), `README.en.md is missing ${heading}`)
}
for (const screenshot of [
  '01-api-client-board.png',
  '02-api-client-modify.png',
  '03-api-client-help.png',
  '04-api-client-demo.png',
  '05-travel-app-board.png',
  '06-travel-app-demo.png',
]) {
  const relativePath = `docs/screenshots/${screenshot}`
  assert.ok(readmeSource.includes(`](${relativePath})`), `README.md must embed ${relativePath}`)
  assert.ok(readmeEnSource.includes(`](${relativePath})`), `README.en.md must embed ${relativePath}`)
  const image = await readFile(join(root, relativePath))
  assert.ok(image.length > 0, `${relativePath} must not be empty`)
}
assert.match(readmeSource, /无需构建/, 'README.md must explain the v2 no-build workflow')
assert.match(readmeEnSource, /no build step/i, 'README.en.md must explain the v2 no-build workflow')
assert.doesNotMatch(readmeSource, /\.\/build\.command|\bbuild\.cmd\b/, 'README.md must not instruct v2 users to run v1 build scripts')
assert.doesNotMatch(readmeEnSource, /\.\/build\.command|\bbuild\.cmd\b/, 'README.en.md must not instruct v2 users to run v1 build scripts')

const results = []
results.push(await checkProject(starter))
results.push(await checkProject(join(root, 'demo/api-client'), {
  frameworkDirectory: join(starter, 'framework'),
  delivery: false,
}))
results.push(await checkProject(join(root, 'demo/travel-app'), {
  frameworkDirectory: join(starter, 'framework'),
  delivery: false,
}))

async function relativeFiles(directory) {
  const entries = await readdir(directory, { recursive: true, withFileTypes: true })
  return entries
    .filter((entry) => entry.isFile() && entry.name !== '.DS_Store')
    .map((entry) => join(entry.parentPath, entry.name).slice(directory.length + 1))
    .sort()
}

const starterFrameworkFiles = await relativeFiles(join(starter, 'framework'))
assert.ok(!starterFrameworkFiles.some((file) => /\.(?:jsx|tsx|ts)$/i.test(file)), 'starter framework contains maintenance source')
const frameworkSourceFiles = await relativeFiles(frameworkSource)
assert.ok(frameworkSourceFiles.includes('bridge-entry.jsx'), 'framework-source/bridge-entry.jsx is missing')
assert.ok(frameworkSourceFiles.some((file) => file.startsWith('react-source/board/')), 'framework-source Board source is missing')
assert.ok(frameworkSourceFiles.some((file) => file.startsWith('react-source/core/')), 'framework-source core source is missing')
assert.ok(frameworkSourceFiles.some((file) => file.startsWith('react-source/ui/')), 'framework-source UI source is missing')
assert.ok(!frameworkSourceFiles.some((file) => /^(?:runtime|styles|vendor)\//.test(file)), 'framework-source must not contain deliverable runtime mirrors')
const bridgeSource = await readFile(join(frameworkSource, 'bridge-entry.jsx'), 'utf8')
assert.match(bridgeSource, /from '\.\/react-source\//, 'bridge-entry.jsx must import its colocated maintenance source')

for (const demoName of ['api-client', 'travel-app']) {
  const html = await readFile(join(root, 'demo', demoName, 'index.html'), 'utf8')
  assert.match(html, /\.\.\/\.\.\/starter\/framework\//, `${demoName} must share starter/framework`)
  assert.doesNotMatch(html, /\.\.\/\.\.\/framework\//, `${demoName} still references the preview framework`)
  assert.match(html, /COVERAGE FIXTURE ONLY/, `${demoName} must warn that its framework path is demo-only`)
}

const rootNames = await readdir(root)
for (const stalePreview of ['framework', 'src', 'index.html', 'EDITING.md']) {
  assert.ok(!rootNames.includes(stalePreview), `root preview mirror must not exist: ${stalePreview}`)
}

const starterNames = await readdir(starter)
assert.ok(!starterNames.includes('SKILL.md'), 'starter must not contain Skill authoring files')
assert.ok(!starterNames.includes('scripts') && !starterNames.includes('tools'), 'starter must not contain maintenance tools')

const totalScreens = results.slice(0, 3).reduce((sum, result) => sum + result.screenCount, 0)
console.log(`vue-global skill: pass (${results.length} deliverable/demo projects, ${totalScreens} screens, v${version})`)
