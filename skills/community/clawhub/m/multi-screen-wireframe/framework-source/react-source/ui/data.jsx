import { useFlowTarget } from './flow.js'

export function Cell({ to, onClick, title, subtitle, value, className = '', children, ...rest }) {
  const flow = useFlowTarget(to, onClick)
  return (
    <div
      className={`wf-cell ${to ? 'wf-interactive' : ''} ${className}`.trim()}
      role={to ? 'link' : rest.role}
      tabIndex={to && rest.tabIndex === undefined ? 0 : rest.tabIndex}
      {...rest}
      {...flow}
    >
      <div className="wf-cell-main">
        <strong className="wf-cell-title">{title}</strong>
        {subtitle ? <span className="wf-cell-subtitle">{subtitle}</span> : null}
        {children}
      </div>
      {value !== undefined ? <span className="wf-cell-value">{value}</span> : null}
    </div>
  )
}

export function DataTable({ columns = [], rows = [], getRowKey, className = '', ...rest }) {
  return (
    <div className={`wf-table-wrap ${className}`.trim()} {...rest}>
      <table className="wf-table">
        <thead className="wf-table-head">
          <tr className="wf-table-header-row">
            {columns.map((column) => (
              <th className="wf-table-heading" data-wf-key={column.key} key={column.key}>{column.label}</th>
            ))}
          </tr>
        </thead>
        <tbody className="wf-table-body">
          {rows.map((row, index) => {
            const rowKey = getRowKey ? getRowKey(row) : row.id || index
            return (
              <tr className="wf-table-row" data-wf-key={rowKey} key={rowKey}>
                {columns.map((column) => (
                  <td className="wf-table-cell" data-wf-key={column.key} key={column.key}>
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export function Tabs({ items = [], activeId, onChange, className = '', ...rest }) {
  return (
    <div className={`wf-tabs ${className}`.trim()} role="tablist" {...rest}>
      {items.map((item) => (
        <button
          className="wf-tab-control"
          type="button"
          role="tab"
          aria-selected={item.id === activeId}
          key={item.id}
          onClick={() => onChange?.(item.id)}
        >
          {item.label}
        </button>
      ))}
    </div>
  )
}

export function Steps({
  items = [],
  current = 0,
  direction = 'horizontal',
  className = '',
  ...rest
}) {
  const vertical = direction === 'vertical'
  return (
    <ol
      className={`wf-steps ${vertical ? 'wf-steps-vertical' : 'wf-steps-horizontal'} ${className}`.trim()}
      {...rest}
    >
      {items.map((item, index) => {
        const status = index < current ? 'done' : index === current ? 'current' : 'todo'
        return (
          <li className={`wf-steps-item wf-steps-item-${status}`} key={item.id || item.label || index}>
            <div className="wf-steps-indicator">
              <span className="wf-step-mark" aria-hidden="true">
                {status === 'done' ? null : index + 1}
              </span>
              {index < items.length - 1 ? <span className="wf-steps-line" aria-hidden="true" /> : null}
            </div>
            <div className="wf-steps-content">
              <span className="wf-steps-label">{item.label}</span>
              {item.description ? <span className="wf-steps-desc">{item.description}</span> : null}
            </div>
          </li>
        )
      })}
    </ol>
  )
}

export function EmptyState({ title, description, action, className = '', ...rest }) {
  return (
    <div className={`wf-empty-state ${className}`.trim()} {...rest}>
      <span className="wf-empty-icon" aria-hidden="true" />
      {title ? <strong className="wf-empty-title">{title}</strong> : null}
      {description ? <p className="wf-empty-desc">{description}</p> : null}
      {action ? <div className="wf-empty-action">{action}</div> : null}
    </div>
  )
}
