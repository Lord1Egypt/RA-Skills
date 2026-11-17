import { Button } from './forms.jsx'

function ScreenPortal({ children }) {
  const anchor = React.useRef(null)
  const [host, setHost] = React.useState(null)

  React.useLayoutEffect(() => {
    setHost(anchor.current?.closest('.wf-screen-content') || null)
  }, [])

  if (!host) return <span ref={anchor} className="wf-overlay-anchor" aria-hidden="true" />
  return ReactDOM.createPortal(children, host)
}

export function Modal({ open, title, children, actions, onClose, className = '', ...rest }) {
  if (!open) return null
  return (
    <ScreenPortal>
      <div className={`wf-overlay wf-modal-overlay ${className}`.trim()} role="presentation" {...rest}>
        <section className="wf-modal" role="dialog" aria-modal="true" aria-label={title}>
          <header className="wf-modal-header">
            <strong className="wf-modal-title">{title}</strong>
            {onClose ? <Button onClick={onClose}>关闭</Button> : null}
          </header>
          <div className="wf-modal-body">{children}</div>
          {actions ? <footer className="wf-modal-footer">{actions}</footer> : null}
        </section>
      </div>
    </ScreenPortal>
  )
}

export function ConfirmDialog({
  open,
  title = '确认操作',
  message,
  confirmLabel = '确认',
  cancelLabel = '取消',
  onConfirm,
  onCancel,
  className = '',
  ...rest
}) {
  return (
    <Modal
      open={open}
      title={title}
      className={className}
      onClose={onCancel}
      {...rest}
      actions={(
        <>
          <Button onClick={onCancel}>{cancelLabel}</Button>
          <Button variant="primary" onClick={onConfirm}>{confirmLabel}</Button>
        </>
      )}
    >
      <p className="wf-confirm-message">{message}</p>
    </Modal>
  )
}

export function Toast({ open, children, className = '', ...rest }) {
  if (!open) return null
  return (
    <ScreenPortal>
      <div className={`wf-overlay wf-toast ${className}`.trim()} role="status" {...rest}>{children}</div>
    </ScreenPortal>
  )
}

export function LoadingOverlay({ open, label = '加载中', className = '', ...rest }) {
  if (!open) return null
  return (
    <ScreenPortal>
      <div className={`wf-overlay wf-loading ${className}`.trim()} role="status" {...rest}>
        <span className="wf-loading-shape" aria-hidden="true" />
        <span className="wf-loading-label">{label}</span>
      </div>
    </ScreenPortal>
  )
}
