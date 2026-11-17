import { useFlowTarget } from './flow.js'

export function WireMap({ className = '', style, children, ...rest }) {
  return (
    <div className={`wf-map ${className}`.trim()} style={{ position: 'relative', ...style }} {...rest}>
      <span className="wf-map-line wf-map-line-a" aria-hidden="true" />
      <span className="wf-map-line wf-map-line-b" aria-hidden="true" />
      {children}
    </div>
  )
}

export function MapMarker({ x, y, label, to, onClick, className = '', style, ...rest }) {
  const flow = useFlowTarget(to, onClick)
  return (
    <button
      type="button"
      className={`wf-map-marker ${className}`.trim()}
      aria-label={label}
      style={{ left: `${x}%`, top: `${y}%`, ...style }}
      {...rest}
      {...flow}
    >
      <span className="wf-map-marker-shape" aria-hidden="true" />
    </button>
  )
}

export function MapOverlay({ position = 'bottom', className = '', children, ...rest }) {
  return (
    <div className={`wf-map-overlay wf-map-overlay-${position} ${className}`.trim()} {...rest}>
      {children}
    </div>
  )
}
