export default function MetricCard({ label, value, unit, icon, iconType = 'blue', valueColor, foot }) {
  const iconClass = iconType === 'orange' ? 'icon-orange' : iconType === 'green' ? 'icon-green' : ''
  
  return (
    <div className="metric-card">
      <div className="metric-head">
        <span className="metric-label">{label}</span>
        <div className={`icon-tile ${iconClass}`}>{icon}</div>
      </div>
      <div className="metric-value" style={{ color: valueColor }}>
        {value}
        {unit && <span style={{ fontSize: '18px' }}>{unit}</span>}
      </div>
      <div className="metric-foot">{foot}</div>
    </div>
  )
}
