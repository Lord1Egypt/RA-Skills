import { usePrototype } from '../core/PrototypeContext.jsx'
import { useFlowTarget } from './flow.js'

function joinClass(base, extra) {
  return extra ? `${base} ${extra}` : base
}

function resolveColumns(columns, viewportKey) {
  const value =
    columns && typeof columns === 'object' && !Array.isArray(columns)
      ? columns[viewportKey]
      : columns
  if (Number.isInteger(value) && value > 0) return `repeat(${value}, minmax(0, 1fr))`
  if (typeof value === 'string' && value.trim()) return value
  throw new Error('Grid columns must resolve to a positive integer or non-empty CSS string')
}

function useLayoutFlow(to, onClick, rest) {
  const flow = useFlowTarget(to, onClick)
  return {
    classNameSuffix: to ? ' wf-interactive' : '',
    role: to ? 'link' : rest.role,
    tabIndex: to && rest.tabIndex === undefined ? 0 : rest.tabIndex,
    flow,
  }
}

export function Box({ className, style, children, to, onClick, ...rest }) {
  const { classNameSuffix, role, tabIndex, flow } = useLayoutFlow(to, onClick, rest)
  return (
    <div
      className={joinClass(`wf-box${classNameSuffix}`, className)}
      role={role}
      tabIndex={tabIndex}
      style={{ ...style }}
      {...rest}
      {...flow}
    >
      {children}
    </div>
  )
}

export function Row({
  className,
  style,
  children,
  gap = 0,
  alignItems = 'stretch',
  justifyContent = 'flex-start',
  to,
  onClick,
  ...rest
}) {
  const { classNameSuffix, role, tabIndex, flow } = useLayoutFlow(to, onClick, rest)
  const mergedStyle = {
    display: 'flex',
    flexDirection: 'row',
    gap,
    alignItems,
    justifyContent,
    ...style,
  }
  return (
    <div
      className={joinClass(`wf-row${classNameSuffix}`, className)}
      role={role}
      tabIndex={tabIndex}
      style={mergedStyle}
      {...rest}
      {...flow}
    >
      {children}
    </div>
  )
}

export function Column({
  className,
  style,
  children,
  gap = 0,
  alignItems = 'stretch',
  justifyContent = 'flex-start',
  to,
  onClick,
  ...rest
}) {
  const { classNameSuffix, role, tabIndex, flow } = useLayoutFlow(to, onClick, rest)
  const mergedStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap,
    alignItems,
    justifyContent,
    ...style,
  }
  return (
    <div
      className={joinClass(`wf-column${classNameSuffix}`, className)}
      role={role}
      tabIndex={tabIndex}
      style={mergedStyle}
      {...rest}
      {...flow}
    >
      {children}
    </div>
  )
}

export function Grid({ className, style, children, columns = 1, gap = 0, to, onClick, ...rest }) {
  const { viewportKey } = usePrototype()
  const { classNameSuffix, role, tabIndex, flow } = useLayoutFlow(to, onClick, rest)
  const mergedStyle = {
    display: 'grid',
    gridTemplateColumns: resolveColumns(columns, viewportKey),
    gap,
    ...style,
  }
  return (
    <div
      className={joinClass(`wf-grid${classNameSuffix}`, className)}
      role={role}
      tabIndex={tabIndex}
      style={mergedStyle}
      {...rest}
      {...flow}
    >
      {children}
    </div>
  )
}
