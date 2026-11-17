export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error, info) {
    console.error(`[wireframe:${this.props.scope || 'unknown'}]`, error, info)
  }

  componentDidUpdate(previousProps) {
    if (this.state.error && previousProps.resetKey !== this.props.resetKey) {
      this.setState({ error: null })
    }
  }

  render() {
    if (!this.state.error) return this.props.children
    const { screenId, source, scope } = this.props
    return (
      <div className="wf-error-card" role="alert">
        <strong>{scope === 'screen' ? `Screen: ${screenId}` : 'Board error'}</strong>
        {source ? <span>Source: {source}</span> : null}
        <span>Message: {this.state.error.message}</span>
        <pre>{this.state.error.stack}</pre>
      </div>
    )
  }
}
