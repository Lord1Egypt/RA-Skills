export default function Home() {
  return (
    <div className="workspace-body full-width">
      <main className="content-host">
        <div className="content-surface" style={{ minHeight: 'calc(100vh - 124px)' }}>
          <div className="page-headline">
            <div>
              <h1>首页</h1>
              <p>欢迎使用新能源 EPC 成本管理系统</p>
            </div>
          </div>
          <div className="page-panel">
            <div className="panel-head">
              <span className="panel-title">系统概览</span>
            </div>
            <p className="muted-text">这里是首页内容，没有左侧边栏，内容区域占满全宽。</p>
          </div>
        </div>
      </main>
    </div>
  )
}
