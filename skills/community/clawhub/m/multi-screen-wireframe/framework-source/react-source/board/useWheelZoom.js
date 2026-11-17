import { clampScale, shouldZoomOnWheel } from './navigation.js'

const TRACKPAD_ZOOM_RATE = 0.0015

function normalizedWheelDelta(event) {
  if (event.deltaMode === 1) return event.deltaY * 16
  if (event.deltaMode === 2) return event.deltaY * 100
  return event.deltaY
}

export function nextWheelScale(scale, event, { trackpadMode = false, sensitivity = 0.6 } = {}) {
  if (!trackpadMode) return clampScale(scale * (event.deltaY > 0 ? 0.9 : 1.1))
  const delta = normalizedWheelDelta(event)
  if (!delta) return scale
  return clampScale(scale * Math.exp(-delta * TRACKPAD_ZOOM_RATE * sensitivity))
}

/** 绑定非 passive wheel，才能合法 preventDefault（React onWheel 默认 passive）。 */
export function bindWheelZoom(
  el,
  getScale,
  setScale,
  getLocked = () => false,
  getOptions = () => ({}),
) {
  if (!el) return () => {}
  const onWheel = (event) => {
    if (!shouldZoomOnWheel(event, { locked: getLocked() })) return
    event.preventDefault()
    setScale(nextWheelScale(getScale(), event, getOptions()))
  }
  el.addEventListener('wheel', onWheel, { passive: false })
  return () => el.removeEventListener('wheel', onWheel)
}

export function useWheelZoom(elementRef, scale, setScale, locked = false, options = {}) {
  const scaleRef = React.useRef(scale)
  const lockedRef = React.useRef(locked)
  const optionsRef = React.useRef(options)
  scaleRef.current = scale
  lockedRef.current = locked
  optionsRef.current = options

  React.useEffect(
    () => bindWheelZoom(
      elementRef.current,
      () => scaleRef.current,
      setScale,
      () => lockedRef.current,
      () => optionsRef.current,
    ),
    [elementRef, setScale],
  )
}
