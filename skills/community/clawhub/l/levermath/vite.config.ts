import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

const root = fileURLToPath(new URL('.', import.meta.url))
const examples = new Set(['origami-ellipse', 'vector-p-norm'])
const fontLicenses = [
  ['Latin Modern · GUST Font License', 'licenses/GUST-FONT-LICENSE.TXT'],
  ['Latin Modern · LPPL 1.3c', 'licenses/LPPL-1.3c.txt'],
  ['Noto Serif SC · SIL OFL 1.1', 'licenses/Noto-Serif-SC-OFL-1.1.txt'],
] as const
const componentLicenses = [
  ['LeverMaTH', 'LICENSE'],
  ['JSXGraph', 'licenses/JSXGraph-LICENSE.MIT.txt'],
  ['KaTeX 与其字体', 'licenses/KaTeX-LICENSE.txt'],
] as const

function escapeHtml(value: string): string {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function licenseBlock(title: string, file: string): string {
  const text = readFileSync(resolve(root, file), 'utf8')
  return `<h3>${escapeHtml(title)}</h3><pre>${escapeHtml(text)}</pre>`
}

function licensePanel(): string {
  const notices = fontLicenses.map(([title, file]) => licenseBlock(title, file)).join('')
  // 字体许可直接展开；组件许可文本随单文件保留但不渲染，避免设置面板混杂。
  const components = componentLicenses.map(([title, file]) => licenseBlock(title, file)).join('')

  return `<details id="levermath-licenses"><summary>字体许可</summary><div><button type="button" onclick="this.closest('details').removeAttribute('open')" style="float:right;margin-left:12px">收起</button></div>${notices}</details><template id="levermath-component-licenses">${components}</template>`
}

// 开发阶段源码分离；发布时 JS、CSS、图片、字体与必要的许可文本一并内联。
export default defineConfig(({ mode }) => {
  const example = examples.has(mode) ? mode : null
  return {
    root: example ? resolve(root, 'examples', example) : root,
    base: './',
    plugins: [
      viteSingleFile(),
      {
        name: 'levermath-licenses',
        apply: 'build',
        transformIndexHtml(html: string) {
          return html.replace('</body>', `${licensePanel()}\n</body>`)
        },
      },
    ],
    build: {
      outDir: resolve(root, 'dist', ...(example ? ['examples', example] : [])),
      emptyOutDir: true,
      target: 'es2019',
      cssCodeSplit: false,
      assetsInlineLimit: 100_000_000,
    },
  }
})
