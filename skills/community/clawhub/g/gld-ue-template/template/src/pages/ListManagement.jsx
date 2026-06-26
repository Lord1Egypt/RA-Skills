import { useState, useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'
import MetricCard from '../components/MetricCard'
import Tag from '../components/Tag'
import ProgressBar from '../components/ProgressBar'

export default function ListManagement() {
  const [activeTab, setActiveTab] = useState('list')
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (activeTab === 'timeline' && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }
      
      const ctx = chartRef.current.getContext('2d')
      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['9月', '10月', '11月', '12月', '1月', '2月', '3月'],
          datasets: [{
            label: '累计到货量',
            data: [0, 5000, 13000, 20000, 28000, 36000, 40000],
            borderColor: '#3c83f8',
            backgroundColor: 'rgba(60, 131, 248, 0.1)',
            yAxisID: 'y',
            tension: 0.3,
            fill: true
          }, {
            label: '累计安装量',
            data: [0, 800, 4800, 12000, 18000, 25000, 32000],
            borderColor: '#46bc46',
            backgroundColor: 'rgba(70, 188, 70, 0.1)',
            yAxisID: 'y1',
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          plugins: {
            legend: { position: 'top' }
          },
          scales: {
            y: {
              type: 'linear',
              position: 'left',
              title: { display: true, text: '到货量(块)' }
            },
            y1: {
              type: 'linear',
              position: 'right',
              title: { display: true, text: '安装量(块)' },
              grid: { drawOnChartArea: false }
            }
          }
        }
      })
    }
    
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }
    }
  }, [activeTab])

  return (
    <>
      <div className="crumb-row">
        <span className="breadcrumb">首页</span>
        <span>/</span>
        <span className="breadcrumb">清单管理</span>
        <span>/</span>
        <span className="breadcrumb current">动态清单归集</span>
      </div>

      <div className="content-surface">
        <div className="page-headline">
          <div>
            <h1>动态清单归集</h1>
            <p>光伏组件采购及安装工程项目 · 合同执行中</p>
          </div>
          <div className="headline-actions">
            <button className="primary-button">导出报表</button>
            <button className="ghost-button">打印</button>
          </div>
        </div>

        <div className="tab-strip">
          <button 
            className={`tab ${activeTab === 'list' ? 'active' : ''}`} 
            onClick={() => setActiveTab('list')}
          >
            清单视图
          </button>
          <button 
            className={`tab ${activeTab === 'timeline' ? 'active' : ''}`} 
            onClick={() => setActiveTab('timeline')}
          >
            时间线分析
          </button>
          <button 
            className={`tab ${activeTab === 'deviation' ? 'active' : ''}`} 
            onClick={() => setActiveTab('deviation')}
          >
            偏差分析
          </button>
          <button 
            className={`tab ${activeTab === 'composition' ? 'active' : ''}`} 
            onClick={() => setActiveTab('composition')}
          >
            构成分析
          </button>
        </div>

        {activeTab === 'list' && (
          <div className="tab-panel active">
            <div className="metric-grid" style={{ marginBottom: '20px' }}>
              <MetricCard 
                label="收入合同总额" 
                value="2.8" 
                unit="亿" 
                icon="¥" 
                foot="含税合同价" 
              />
              <MetricCard 
                label="合同偏差金额" 
                value="-700" 
                unit="万" 
                icon="Δ" 
                iconType="orange"
                valueColor="#ef5f59"
                foot="动态成本 - 合同金额" 
              />
              <MetricCard 
                label="合同偏差率" 
                value="-2.5" 
                unit="%" 
                icon="%" 
                iconType="orange"
                valueColor="#ef5f59"
                foot="偏差 / 合同金额" 
              />
              <MetricCard 
                label="内控成本总额" 
                value="2.52" 
                unit="亿" 
                icon="◈" 
                iconType="green"
                foot="企业内部预算" 
              />
            </div>

            <div className="toolbar">
              <div className="toolbar-left">
                <input type="text" className="field" placeholder="搜索清单编号或名称" style={{ width: '220px' }} />
                <select className="field" style={{ width: '160px' }}>
                  <option value="">全部分类</option>
                  <option value="E1">设备及安装工程-设备购置</option>
                  <option value="E2">设备及安装工程-建安工程</option>
                  <option value="A">建筑工程</option>
                  <option value="O">其他费用</option>
                </select>
              </div>
              <div className="toolbar-right">
                <button className="ghost-button">全部展开</button>
                <button className="ghost-button">全部折叠</button>
              </div>
            </div>

            <div className="table-card">
              <table>
                <thead>
                  <tr>
                    <th style={{ width: '120px' }}>编号</th>
                    <th style={{ textAlign: 'left' }}>清单名称</th>
                    <th style={{ width: '60px' }}>单位</th>
                    <th style={{ width: '100px' }}>合同单价</th>
                    <th style={{ width: '100px' }}>合同量</th>
                    <th style={{ width: '100px' }}>到货量</th>
                    <th style={{ width: '140px' }}>进度完成量</th>
                    <th style={{ width: '80px' }}>到货进度</th>
                    <th style={{ width: '80px' }}>安装进度</th>
                    <th style={{ width: '120px' }}>动态成本</th>
                    <th style={{ width: '100px', textAlign: 'right' }}>成本偏差</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="category-row category-E1" style={{ cursor: 'pointer' }}>
                    <td colSpan="2"><span style={{ marginRight: '8px', fontSize: '10px' }}>▼</span>一、设备及安装工程-设备购置</td>
                    <td style={{ textAlign: 'center' }}>-</td>
                    <td style={{ textAlign: 'right' }}>-</td>
                    <td style={{ textAlign: 'right' }}>-</td>
                    <td style={{ textAlign: 'right' }}>-</td>
                    <td style={{ textAlign: 'center' }}>
                      <div className="progress-cell">
                        <ProgressBar percent={45} />
                        <span>45%</span>
                      </div>
                    </td>
                    <td style={{ textAlign: 'center' }}>-</td>
                    <td style={{ textAlign: 'center' }}>-</td>
                    <td style={{ textAlign: 'right' }}>¥1.24亿</td>
                    <td style={{ textAlign: 'right', color: '#ef5f59' }}>-2.5%</td>
                  </tr>
                  <tr className="deviation-high" style={{ cursor: 'pointer' }}>
                    <td>E-01-001</td>
                    <td>单晶双面545Wp光伏组件</td>
                    <td style={{ textAlign: 'center' }}>块</td>
                    <td style={{ textAlign: 'right' }}>¥1.40</td>
                    <td style={{ textAlign: 'right' }}>40,000</td>
                    <td style={{ textAlign: 'right' }}>20,000</td>
                    <td style={{ textAlign: 'center' }}>
                      <div className="progress-cell">
                        <ProgressBar percent={45} warning={true} />
                        <span>45%</span>
                      </div>
                    </td>
                    <td style={{ textAlign: 'center' }}>50%</td>
                    <td style={{ textAlign: 'center' }}>45%</td>
                    <td style={{ textAlign: 'right' }}>¥2,718.00万</td>
                    <td style={{ textAlign: 'right', color: '#ef5f59' }}>-8.0%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="tab-panel active">
            <div className="page-panel">
              <div className="panel-head">
                <span className="panel-title">到货量与安装量趋势</span>
              </div>
              <div style={{ height: '300px' }}>
                <canvas ref={chartRef}></canvas>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'deviation' && (
          <div className="tab-panel active">
            <div className="page-panel">
              <div className="panel-head">
                <span className="panel-title">偏差分析</span>
              </div>
              <p className="muted-text">偏差分析内容...</p>
            </div>
          </div>
        )}
        
        {activeTab === 'composition' && (
          <div className="tab-panel active">
            <div className="page-panel">
              <div className="panel-head">
                <span className="panel-title">构成分析</span>
              </div>
              <p className="muted-text">构成分析内容...</p>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
