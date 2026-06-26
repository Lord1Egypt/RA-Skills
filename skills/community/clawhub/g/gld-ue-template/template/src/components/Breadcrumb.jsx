import { useLocation, NavLink } from 'react-router-dom'

const breadcrumbMap = {
  '/': '首页',
  '/list': '清单管理',
  '/list/dynamic': '动态清单归集',
  '/list/ledger': '清单台账',
  '/list/changes': '变更记录',
  '/analysis': '分析视图',
  '/analysis/deviation': '成本偏差分析',
  '/analysis/progress': '进度跟踪',
  '/analysis/forecast': '预测分析',
  '/settings': '系统设置',
  '/settings/master': '基础数据',
  '/settings/users': '用户管理',
}

export default function Breadcrumb() {
  const location = useLocation()
  const pathnames = location.pathname.split('/').filter((x) => x)

  const crumbs = pathnames.reduce((crumbsSoFar, _, index) => {
    const breadcrumbPath = '/' + pathnames.slice(0, index + 1).join('/')
    const breadcrumbName = breadcrumbMap[breadcrumbPath]
    if (breadcrumbName) {
      crumbsSoFar.push({ path: breadcrumbPath, name: breadcrumbName })
    }
    return crumbsSoFar
  }, [])

  if (crumbs.length === 0) return null

  return (
    <div className="crumb-row">
      {crumbs.map((crumb, index) => {
        const isLast = index === crumbs.length - 1
        return (
          <React.Fragment key={crumb.path}>
            {index > 0 && <span>/</span>}
            {isLast ? (
              <span className="breadcrumb current">{crumb.name}</span>
            ) : (
              <NavLink to={crumb.path} className="breadcrumb">
                {crumb.name}
              </NavLink>
            )}
          </React.Fragment>
        )
      })}
    </div>
  )
}
