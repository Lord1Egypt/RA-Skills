import { useFlowTarget } from './flow.js'

export function Heading({ level = 2, className = '', children, ...rest }) {
  const tag = `h${Math.min(6, Math.max(1, level))}`
  return React.createElement(tag, { className: `wf-heading ${className}`.trim(), ...rest }, children)
}

export function Text({ as = 'p', className = '', children, ...rest }) {
  return React.createElement(as, { className: `wf-text ${className}`.trim(), ...rest }, children)
}

export function Card({ to, onClick, className = '', children, ...rest }) {
  const flow = useFlowTarget(to, onClick)
  return (
    <div
      className={`wf-card ${to ? 'wf-interactive' : ''} ${className}`.trim()}
      role={to ? 'link' : rest.role}
      tabIndex={to && rest.tabIndex === undefined ? 0 : rest.tabIndex}
      {...rest}
      {...flow}
    >
      {children}
    </div>
  )
}

export function Badge({ className = '', children, ...rest }) {
  return <span className={`wf-badge ${className}`.trim()} {...rest}>{children}</span>
}

export function Avatar({ size = 40, label, className = '', style, ...rest }) {
  return (
    <div
      className={`wf-avatar ${className}`.trim()}
      aria-label={label}
      style={{ width: size, height: size, ...style }}
      {...rest}
    />
  )
}

export function ImagePlaceholder({
  width = '100%',
  height = 160,
  borderRadius = 0,
  className = '',
  style,
  ...rest
}) {
  return (
    <div
      className={`wf-image-placeholder ${className}`.trim()}
      aria-hidden="true"
      style={{ width, height, borderRadius, ...style }}
      {...rest}
    >
      <span className="wf-placeholder-block" />
    </div>
  )
}
