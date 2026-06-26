export default function StageCard({ name, value, foot, progress, progressColor }) {
  return (
    <div className="stage-card">
      <div className="stage-name">{name}</div>
      {progress !== undefined && (
        <div className="progress-bar" style={{ marginBottom: '8px' }}>
          <span style={{ width: `${progress}%`, background: progressColor }}></span>
        </div>
      )}
      <div style={{ fontSize: '24px', fontWeight: 450, color: '#315282' }}>{value}</div>
      <div className="muted-text">{foot}</div>
    </div>
  )
}
