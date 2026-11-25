import katex from 'katex'
import 'katex/dist/katex.min.css'

// 一切变量与公式都走 KaTeX：帧里写 <span data-tex="F_1"></span>，这里统一渲染。
// 行间公式加 data-display="1"。KaTeX 是纯前端，不需要 LaTeX，字体随单文件内联。
export function mountMath(root: ParentNode = document): void {
  root.querySelectorAll<HTMLElement>('[data-tex]').forEach((el) => {
    const tex = el.dataset.tex
    if (!tex || el.dataset.rendered === '1') return
    katex.render(tex, el, {
      throwOnError: false,
      displayMode: el.dataset.display === '1',
      output: 'html',
    })
    el.dataset.rendered = '1'
  })
}
