import { useFlowTarget } from './flow.js'

export function Button({ to, onClick, variant = 'default', className = '', children, ...rest }) {
  const flow = useFlowTarget(to, onClick)
  return (
    <button
      type="button"
      className={`wf-button wf-button-${variant} ${className}`.trim()}
      {...rest}
      {...flow}
    >
      {children}
    </button>
  )
}

export function TextInput({ className = '', ...rest }) {
  return <input className={`wf-input ${className}`.trim()} type="text" {...rest} />
}

export function TextArea({ className = '', ...rest }) {
  return <textarea className={`wf-input wf-textarea ${className}`.trim()} {...rest} />
}

export function Select({ className = '', children, ...rest }) {
  return <select className={`wf-input wf-select ${className}`.trim()} {...rest}>{children}</select>
}

function Choice({ type, label, className = '', ...rest }) {
  return (
    <label className={`wf-choice ${className}`.trim()}>
      <input className="wf-choice-input" type={type} {...rest} />
      <span className="wf-choice-label">{label}</span>
    </label>
  )
}

export function Checkbox(props) {
  return <Choice type="checkbox" {...props} />
}

export function Radio(props) {
  return <Choice type="radio" {...props} />
}

export function Toggle({ checked = false, onChange, label, className = '', ...rest }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      className={`wf-toggle ${className}`.trim()}
      onClick={(event) => onChange?.(!checked, event)}
      {...rest}
    >
      <span className="wf-toggle-track"><span className="wf-toggle-thumb" /></span>
      {label ? <span className="wf-toggle-label">{label}</span> : null}
    </button>
  )
}

export function FormField({ label, htmlFor, hint, error, className = '', children, ...rest }) {
  return (
    <div className={`wf-form-field ${className}`.trim()} {...rest}>
      <label className="wf-field-label" htmlFor={htmlFor}>{label}</label>
      {children}
      {hint && !error ? <span className="wf-field-hint">{hint}</span> : null}
      {error ? <span className="wf-field-error" role="alert">{error}</span> : null}
    </div>
  )
}
