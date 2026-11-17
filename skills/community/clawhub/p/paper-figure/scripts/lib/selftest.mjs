// scripts/lib/selftest.mjs
// 离线自检：真跑一遍 init → spec → render → chart，再把产物按「能不能上交」的标准验一遍。
//
// 不联网、不花钱、不碰用户数据：全程在系统临时目录里做，跑完删掉。
// 用法：node scripts/lib/selftest.mjs   （npm run smoke 就是它）

import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const ROOT = join(HERE, '..', '..')
const FIG = join(ROOT, 'scripts', 'fig.mjs')

const results = []
let failed = 0

function ok(name, extra = '') {
  results.push({ name, pass: true, extra })
}
function bad(name, error) {
  failed++
  results.push({ name, pass: false, error })
}
function check(name, fn) {
  try {
    const extra = fn()
    ok(name, typeof extra === 'string' ? extra : '')
  } catch (e) {
    bad(name, e?.message || String(e))
  }
}
function assert(cond, msg) {
  if (!cond) throw new Error(msg)
}

function runCli(args) {
  const r = spawnSync(process.execPath, [FIG, ...args], { encoding: 'utf8' })
  let json = null
  try {
    json = JSON.parse(r.stdout)
  } catch {
    json = null
  }
  return { code: r.status, stdout: r.stdout, stderr: r.stderr, json }
}

// ================================================================ 跑流程

const dir = mkdtempSync(join(tmpdir(), 'paper-figure-smoke-'))
let renderResult = null
let chartResult = null

try {
  // 1) init
  let r = runCli(['init', dir])
  check('init 建工作区', () => {
    assert(r.code === 0, `退出码 ${r.code}`)
    assert(r.json && r.json.ok === true, `stdout 不是合法 JSON 或 ok!=true：${r.stdout.slice(0, 200)}`)
    for (const f of ['brief.md', 'figure.json', join('data', 'main.csv'), 'out']) {
      assert(existsSync(join(dir, f)), `缺 ${f}`)
    }
    return r.json.files.length + ' 个文件'
  })

  // 2) spec
  r = runCli(['spec', dir])
  check('spec 解析 brief.md', () => {
    assert(r.code === 0, `退出码 ${r.code}`)
    assert(r.json?.ok === true, `失败：${r.stdout.slice(0, 300)}`)
    assert(r.json.panels >= 1, '没有解析出面板')
    assert(r.json.nodes >= 2, '没有解析出节点')
    return `${r.json.panels} 面板 / ${r.json.nodes} 节点`
  })

  // 3) render
  r = runCli(['render', dir])
  renderResult = r.json
  const svgPath = join(dir, 'out', 'framework-overview-diagram.svg')
  check('render 出 SVG', () => {
    assert(r.code === 0, `退出码 ${r.code}`)
    assert(r.json?.ok === true, `失败：${r.stdout.slice(0, 300)}`)
    assert(existsSync(svgPath), `没生成 ${svgPath}`)
    return `${r.json.widthMm}×${r.json.heightMm}mm`
  })

  if (existsSync(svgPath)) {
    const svg = readFileSync(svgPath, 'utf8')

    check('SVG 根节点带物理尺寸与 mm viewBox', () => {
      const m = svg.match(/width="([\d.]+)mm"\s+height="([\d.]+)mm"\s+viewBox="0 0 ([\d.]+) ([\d.]+)"/)
      assert(m, '根节点没有同时给 width/height(mm) 和 viewBox')
      const [w, h, vw, vh] = [Number(m[1]), Number(m[2]), Number(m[3]), Number(m[4])]
      assert(Math.abs(w - vw) < 0.01, `width ${w}mm 与 viewBox 宽 ${vw} 不一致（1 单位应为 1mm）`)
      assert(Math.abs(h - vh) < 0.01, `height ${h}mm 与 viewBox 高 ${vh} 不一致`)
      return `${w}×${h}mm`
    })

    check('节点/文字带语义属性（check.mjs 依赖）', () => {
      assert(/<g data-node-id="/.test(svg), '没有 data-node-id 的节点分组')
      assert(/data-role="node-label"/.test(svg), '没有 data-role="node-label"')
      assert(/data-font-pt="/.test(svg), '没有 data-font-pt')
      const texts = svg.match(/<text[\s\S]*?<\/text>/g) || []
      const missing = texts.filter((t) => !/data-font-pt="/.test(t)).length
      assert(missing === 0, `${missing} 个 <text> 缺 data-font-pt`)
      return `${texts.length} 段文字`
    })

    check('字号不超过 3 档', () => {
      const sizes = new Set()
      for (const m of svg.matchAll(/data-font-pt="([\d.]+)"/g)) sizes.add(Number(m[1]))
      assert(sizes.size <= 3, `出现 ${sizes.size} 种字号：${[...sizes].join(' / ')}`)
      return [...sizes].sort((a, b) => b - a).join(' / ') + 'pt'
    })

    check('箭头真的画出来（marker + marker-end）', () => {
      assert(/<marker[^>]+id="pf-arrow"/.test(svg), '没有箭头 marker 定义')
      assert(/marker-end="url\(#pf-arrow\)"/.test(svg), '没有引用箭头 marker')
      assert(/markerUnits="strokeWidth"/.test(svg), '箭头没有随线宽缩放')
      return 'ok'
    })

    check('元素没出画布', () => {
      const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/)
      const [W, H] = [Number(m[1]), Number(m[2])]
      let n = 0
      for (const g of svg.matchAll(/data-x="([\d.-]+)" data-y="([\d.-]+)" data-w="([\d.]+)" data-h="([\d.]+)"/g)) {
        const [x, y, w, h] = [Number(g[1]), Number(g[2]), Number(g[3]), Number(g[4])]
        assert(x >= -0.01 && y >= -0.01, `节点越界到负坐标：${x},${y}`)
        assert(x + w <= W + 0.01, `节点右边超出画布：${x + w} > ${W}`)
        assert(y + h <= H + 0.01, `节点下边超出画布：${y + h} > ${H}`)
        n++
      }
      assert(n > 0, '一个节点都没量到')
      return `${n} 个节点在内`
    })

    check('四边留白 ≥3mm，且上下白边合计 ≤12%', () => {
      const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/)
      const W = Number(m[1])
      const H = Number(m[2])
      let top = Infinity
      let bottom = -Infinity
      let left = Infinity
      let right = -Infinity
      for (const g of svg.matchAll(/data-x="([\d.-]+)" data-y="([\d.-]+)" data-w="([\d.]+)" data-h="([\d.]+)"/g)) {
        const [x, y, w, h] = [Number(g[1]), Number(g[2]), Number(g[3]), Number(g[4])]
        top = Math.min(top, y)
        bottom = Math.max(bottom, y + h)
        left = Math.min(left, x)
        right = Math.max(right, x + w)
      }
      // 面板标题文字也要算进去（字顶比节点框更靠上）
      for (const g of svg.matchAll(/<text x="([\d.-]+)" y="([\d.-]+)"[^>]*data-font-pt="([\d.]+)"/g)) {
        const x = Number(g[1])
        const baseline = Number(g[2])
        const pt = Number(g[3])
        top = Math.min(top, baseline - pt * 0.72 * 0.3527778)
        bottom = Math.max(bottom, baseline + pt * 0.21 * 0.3527778)
        left = Math.min(left, x)
        right = Math.max(right, x)
      }
      assert(Number.isFinite(top), '没量到内容')
      const padTop = top
      const padBottom = H - bottom
      const ratio = (padTop + padBottom) / H
      assert(padTop >= 2.9, `上留白 ${padTop.toFixed(2)}mm < 3mm`)
      assert(padBottom >= 2.9, `下留白 ${padBottom.toFixed(2)}mm < 3mm`)
      assert(left >= 2.9, `左留白 ${left.toFixed(2)}mm < 3mm`)
      assert(W - right >= 2.9, `右留白 ${(W - right).toFixed(2)}mm < 3mm`)
      assert(ratio <= 0.12 + 1e-6, `上下白边合计 ${(ratio * 100).toFixed(1)}%（上限 12%）`)
      return `上${padTop.toFixed(1)} 下${padBottom.toFixed(1)} 左${left.toFixed(1)} 右${(W - right).toFixed(1)}mm，合计 ${(ratio * 100).toFixed(1)}%`
    })
  }

  // 4) chart
  r = runCli(['chart', dir])
  chartResult = r.json
  check('chart 出数据图 SVG', () => {
    assert(r.code === 0, `退出码 ${r.code}`)
    assert(r.json?.ok === true, `失败：${r.stdout.slice(0, 300)}`)
    assert(existsSync(r.json.svgPath), 'chart 没写出文件')
    const svg = readFileSync(r.json.svgPath, 'utf8')
    assert(/data-role="axis-label"/.test(svg), '没有坐标轴文字')
    assert(/data-role="series"/.test(svg), '没有数据系列')
    return `${r.json.widthMm}×${r.json.heightMm}mm`
  })

  check('render 与 chart 不互相覆盖', () => {
    assert(renderResult?.svgPath && chartResult?.svgPath, '有一个没出图')
    assert(renderResult.svgPath !== chartResult.svgPath, '两张图写到了同一个文件')
    assert(existsSync(renderResult.svgPath) && existsSync(chartResult.svgPath), '其中一个文件不见了')
    return 'diagram / chart 各写各的'
  })

  // 5) 错误路径也要说人话
  r = runCli(['nope'])
  check('不认识的命令：退出码 1 + {ok:false,fix}', () => {
    assert(r.code === 1, `退出码应为 1，实际 ${r.code}`)
    assert(r.json?.ok === false, 'ok 应为 false')
    assert(r.json.fix, '缺 fix 字段（人话的下一步）')
    return 'ok'
  })

  // 6) platform-tools 的模块可能没落地：应该是「模块未就绪」+ 退出码 2，而不是崩
  if (!existsSync(join(ROOT, 'scripts', 'check.mjs'))) {
    r = runCli(['check', dir])
    check('未落地的 check 命令：退出码 2 + 模块未就绪', () => {
      assert(r.code === 2, `退出码应为 2，实际 ${r.code}`)
      assert(r.json?.error === '模块未就绪', `error 应为「模块未就绪」，实际 ${r.json?.error}`)
      assert(r.json.fix, '缺 fix')
      return 'ok'
    })
  } else {
    r = runCli(['check', dir])
    check('check 命令可调用（模块已就绪）', () => {
      assert(r.code === 0 || r.code === 1, `退出码异常：${r.code}`)
      assert(r.json && typeof r.json === 'object', 'stdout 不是 JSON')
      return `ok=${r.json.ok}`
    })
  }
} finally {
  try {
    rmSync(dir, { recursive: true, force: true })
  } catch {
    /* 临时目录删不掉不影响结论 */
  }
}

// ================================================================ 结果

const pass = results.filter((r) => r.pass).length
console.log('paper-figure 离线自检')
console.log('─'.repeat(64))
for (const r of results) {
  const mark = r.pass ? '✅' : '❌'
  console.log(`${mark} ${r.name}${r.extra ? `（${r.extra}）` : ''}`)
  if (!r.pass) console.log(`   原因：${r.error}`)
}
console.log('─'.repeat(64))
console.log(`${pass}/${results.length} 通过${failed ? `，${failed} 项失败` : ''}`)
if (chartResult?.stats) {
  console.log(`示例数据图：${chartResult.stats.points} 个点 · ${chartResult.stats.series.length} 组 · ${chartResult.stats.kind}`)
}
process.exit(failed ? 1 : 0)
