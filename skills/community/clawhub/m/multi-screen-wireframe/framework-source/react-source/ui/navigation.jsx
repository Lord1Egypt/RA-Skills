import { usePrototype } from '../core/PrototypeContext.jsx'
import { createFlowProps } from './flow.js'

export function PageHeader({ title, titleId, subtitle, subtitleId, actions, className = '', ...rest }) {
  return (
    <header className={`wf-page-header ${className}`.trim()} {...rest}>
      <div className="wf-page-header-copy">
        <h1 id={titleId} className="wf-page-title">{title}</h1>
        {subtitle ? <p id={subtitleId} className="wf-page-subtitle">{subtitle}</p> : null}
      </div>
      {actions ? <div className="wf-page-actions">{actions}</div> : null}
    </header>
  )
}

function NavigationList({ as, items, activeId, className, ...rest }) {
  const { navigate } = usePrototype()
  return React.createElement(
    as,
    { className, ...rest },
    items.map((item) => (
      <button
        type="button"
        key={item.to}
        className={item.to === activeId ? 'wf-nav-item is-active' : 'wf-nav-item'}
        {...createFlowProps(item.to, item.onClick, navigate)}
      >
        <span className="wf-nav-mark" aria-hidden="true" />
        <span className="wf-nav-label">{item.label}</span>
      </button>
    )),
  )
}

export function SideNav({ items = [], activeId, className = '', ...rest }) {
  return (
    <NavigationList
      as="nav"
      items={items}
      activeId={activeId}
      className={`wf-side-nav ${className}`.trim()}
      {...rest}
    />
  )
}

export function TabBar({ items = [], activeId, className = '', ...rest }) {
  const { navigate } = usePrototype()
  return (
    <nav className={`wf-tab-bar ${className}`.trim()} {...rest}>
      {items.map((item) => (
        <button
          type="button"
          key={item.to}
          className={item.to === activeId ? 'wf-tab-item is-active' : 'wf-tab-item'}
          {...createFlowProps(item.to, item.onClick, navigate)}
        >
          <span className="wf-tab-icon" aria-hidden="true" />
          <span className="wf-tab-label">{item.label}</span>
        </button>
      ))}
    </nav>
  )
}

export function Breadcrumbs({ items = [], className = '', ...rest }) {
  const { navigate } = usePrototype()
  return (
    <nav className={`wf-breadcrumbs ${className}`.trim()} aria-label="Breadcrumbs" {...rest}>
      {items.map((item, index) => (
        <React.Fragment key={`${item.label}-${index}`}>
          {index > 0 ? <span className="wf-breadcrumb-divider" aria-hidden="true" /> : null}
          {item.to ? (
            <button className="wf-breadcrumb-link" type="button" {...createFlowProps(item.to, item.onClick, navigate)}>
              {item.label}
            </button>
          ) : <span className="wf-breadcrumb-current">{item.label}</span>}
        </React.Fragment>
      ))}
    </nav>
  )
}

/** 移动端整屏壳：内容区可滚，TabBar 贴底。tabs / activeId 与 TabBar 相同。 */
export function MobileShell({ children, tabs = [], activeId, className = '', ...rest }) {
  return (
    <div className={`wf-mobile-shell ${className}`.trim()} {...rest}>
      <main className="wf-mobile-shell-body">{children}</main>
      {tabs.length > 0 ? <TabBar items={tabs} activeId={activeId} /> : null}
    </div>
  )
}
