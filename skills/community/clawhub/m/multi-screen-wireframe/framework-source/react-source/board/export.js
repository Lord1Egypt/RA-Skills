import { expandScreenContent, measureContentBox } from './expand.js'
import { createTranslator } from './i18n/context.jsx'

let exportLibrariesPromise

const libraries = [
  { file: 'html2canvas.min.js', ready: () => typeof window.html2canvas === 'function' },
  { file: 'jszip.min.js', ready: () => typeof window.JSZip === 'function' },
  { file: 'FileSaver.min.js', ready: () => typeof window.saveAs === 'function' },
]

function loadScript(file, t) {
  return new Promise((resolve, reject) => {
    let existing = document.querySelector(`script[data-wireframe-export="${file}"]`)
    if (existing) {
      if (existing.dataset.wireframeExportState === 'loaded') {
        existing.remove()
        existing = null
      }
    }
    if (existing) {
      existing.addEventListener('load', resolve, { once: true })
      existing.addEventListener('error', reject, { once: true })
      return
    }
    const vendorBase = window.WIREFRAME_VENDOR_BASE
    if (!vendorBase) {
      reject(new Error(t('export.vendorBaseMissing')))
      return
    }
    const script = document.createElement('script')
    script.src = new URL(file, vendorBase).href
    script.dataset.wireframeExport = file
    script.dataset.wireframeExportState = 'loading'
    script.onload = () => {
      script.dataset.wireframeExportState = 'loaded'
      resolve()
    }
    script.onerror = () => {
      script.remove()
      reject(new Error(t('export.libraryLoadFailed', { file })))
    }
    document.head.appendChild(script)
  })
}

export function loadExportLibraries(t = createTranslator('zh-CN')) {
  if (!exportLibrariesPromise) {
    exportLibrariesPromise = libraries.reduce(
      (chain, library) => chain.then(async () => {
        if (!library.ready()) await loadScript(library.file, t)
        if (!library.ready()) throw new Error(t('export.libraryInitFailed', { file: library.file }))
      }),
      Promise.resolve(),
    ).catch((error) => {
      exportLibrariesPromise = undefined
      throw error
    })
  }
  return exportLibrariesPromise
}

export async function captureScreen(screenElement, viewport, { expanded = false } = {}, t = createTranslator('zh-CN')) {
  if (!screenElement) throw new Error(t('export.screenNotFound'))
  await loadExportLibraries(t)

  const sandbox = document.createElement('div')
  sandbox.className = 'wf-export-sandbox'
  const clone = screenElement.cloneNode(true)
  sandbox.appendChild(clone)
  document.body.appendChild(sandbox)

  let width = viewport.width
  let height = viewport.height
  try {
    if (expanded) {
      expandScreenContent(clone)
      const box = measureContentBox(clone)
      width = box.width
      height = box.height
    }
    clone.style.width = `${width}px`
    clone.style.height = `${height}px`
    sandbox.style.width = `${width}px`
    sandbox.style.height = `${height}px`

    const canvas = await window.html2canvas(clone, {
      backgroundColor: '#ffffff',
      width,
      height,
      scale: 2,
      useCORS: false,
      logging: false,
    })
    return await new Promise((resolve, reject) => {
      canvas.toBlob(
        (blob) => blob ? resolve(blob) : reject(new Error(t('export.pngEncodeFailed'))),
        'image/png',
      )
    })
  } finally {
    sandbox.remove()
  }
}

function slug(value) {
  return String(value || 'wireframe')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '') || 'wireframe'
}

export async function exportSelected(screens, t = createTranslator('zh-CN')) {
  if (!Array.isArray(screens) || screens.length === 0) {
    throw new Error(t('export.selectAtLeastOne'))
  }
  await loadExportLibraries(t)
  const captured = []
  for (const screen of screens) {
    captured.push({
      name: `${slug(screen.id)}.png`,
      blob: await captureScreen(screen.element, screen.viewport, {
        expanded: !!screen.expanded,
      }, t),
    })
  }

  if (captured.length === 1) {
    window.saveAs(captured[0].blob, captured[0].name)
    return
  }

  const zip = new window.JSZip()
  captured.forEach((item) => zip.file(item.name, item.blob))
  const blob = await zip.generateAsync({ type: 'blob' })
  window.saveAs(blob, `${slug(screens[0].projectName)}.zip`)
}
