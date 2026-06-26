import { useState, useRef, useCallback, useEffect } from 'react'
import './App.css'

const FEATURES = [
  {
    id: 'restore',
    name: '老照片修复',
    desc: '修复破损老照片，去划痕、去噪点、恢复色彩',
    icon: '📷',
    bg: 'linear-gradient(135deg, #6c5ce7, #a855f7)',
  },
  {
    id: 'portrait',
    name: '人像精修',
    desc: '智能美颜、皮肤优化、五官增强',
    icon: '✨',
    bg: 'linear-gradient(135deg, #f97316, #f43f5e)',
  },
  {
    id: 'landscape',
    name: '风景调色',
    desc: '增强色彩、提升对比度、电影级调色',
    icon: '🏔️',
    bg: 'linear-gradient(135deg, #06b6d4, #3b82f6)',
  },
  {
    id: 'style',
    name: '风格调整',
    desc: '油画、水彩、动漫、赛博朋克等多种风格',
    icon: '🎨',
    bg: 'linear-gradient(135deg, #84cc16, #22d3ee)',
  },
]

const STYLES = [
  { id: 'oil', name: '油画', emoji: '🖼️' },
  { id: 'watercolor', name: '水彩', emoji: '💧' },
  { id: 'sketch', name: '素描', emoji: '✏️' },
  { id: 'anime', name: '动漫', emoji: '🌸' },
  { id: 'cyberpunk', name: '赛博朋克', emoji: '🌃' },
  { id: 'vintage', name: '复古胶片', emoji: '📽️' },
  { id: 'ink', name: '水墨画', emoji: '🏯' },
  { id: 'popart', name: '波普艺术', emoji: '🟡' },
]

export default function App() {
  const [feature, setFeature] = useState(null)
  const [style, setStyle] = useState('oil')
  const [uploadedFile, setUploadedFile] = useState(null)
  const [uploadPreview, setUploadPreview] = useState(null)
  const [resultUrl, setResultUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [step, setStep] = useState('select') // select | upload | result
  const [comparePosition, setComparePosition] = useState(50)
  const [dragging, setDragging] = useState(false)
  const fileInputRef = useRef(null)

  const handleFeatureSelect = (f) => {
    setFeature(f)
    setStep('upload')
    setUploadedFile(null)
    setUploadPreview(null)
    setResultUrl(null)
    setError(null)
  }

  const handleBack = () => {
    setStep('select')
    setFeature(null)
    setUploadedFile(null)
    setUploadPreview(null)
    setResultUrl(null)
    setError(null)
  }

  const handleFileChange = (e) => {
    const file = e.target.files?.[0]
    if (file) processFile(file)
  }

  const processFile = (file) => {
    if (!file.type.startsWith('image/')) {
      setError('请上传图片文件')
      return
    }
    setError(null)
    setUploadedFile(file)
    setResultUrl(null)
    const url = URL.createObjectURL(file)
    setUploadPreview(url)
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files?.[0]
    if (file) processFile(file)
  }, [])

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragging(true)
  }

  const handleDragLeave = () => setDragging(false)

  const handleUpload = async () => {
    if (!uploadedFile || !feature) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('image', uploadedFile)
    formData.append('feature', feature.id)
    if (feature.id === 'style') {
      formData.append('style', style)
    }

    try {
      const res = await fetch('/api/edit', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || '处理失败')
      setResultUrl(data.result)
      setStep('result')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!resultUrl) return
    const a = document.createElement('a')
    a.href = resultUrl
    a.download = `${feature?.id || 'edited'}_result.png`
    a.click()
  }

  useEffect(() => {
    return () => {
      if (uploadPreview) URL.revokeObjectURL(uploadPreview)
    }
  }, [uploadPreview])

  if (step === 'select') {
    return (
      <div className="app">
        <header className="header">
          <h1 className="logo">ImageCraft</h1>
          <p className="subtitle">AI 驱动的图片编辑工作室</p>
        </header>
        <div className="feature-grid">
          {FEATURES.map((f) => (
            <button
              key={f.id}
              className="feature-card"
              onClick={() => handleFeatureSelect(f)}
            >
              <div className="feature-icon" style={{ background: f.bg }}>
                {f.icon}
              </div>
              <h3 className="feature-name">{f.name}</h3>
              <p className="feature-desc">{f.desc}</p>
            </button>
          ))}
        </div>
      </div>
    )
  }

  if (step === 'upload') {
    return (
      <div className="app">
        <header className="header-bar">
          <button className="back-btn" onClick={handleBack}>← 返回</button>
          <h2 className="bar-title">{feature?.name}</h2>
        </header>

        {feature?.id === 'style' && (
          <div className="style-selector">
            {STYLES.map((s) => (
              <button
                key={s.id}
                className={`style-chip ${style === s.id ? 'active' : ''}`}
                onClick={() => setStyle(s.id)}
              >
                {s.emoji} {s.name}
              </button>
            ))}
          </div>
        )}

        <div className="upload-area">
          <div
            className={`dropzone ${dragging ? 'dragging' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
          >
            {uploadPreview ? (
              <img src={uploadPreview} alt="preview" className="preview-img" />
            ) : (
              <div className="dropzone-content">
                <span className="dropzone-icon">📁</span>
                <p>拖拽图片到此处，或点击上传</p>
                <span className="dropzone-hint">支持 JPG、PNG、WEBP</span>
              </div>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </div>

        {error && <div className="error-msg">{error}</div>}

        <button
          className="action-btn"
          disabled={!uploadedFile || loading}
          onClick={handleUpload}
        >
          {loading ? (
            <>
              <span className="spinner" />
              正在处理...
            </>
          ) : (
            `开始${feature?.name}`
          )}
        </button>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header-bar">
        <button className="back-btn" onClick={handleBack}>← 返回</button>
        <h2 className="bar-title">{feature?.name} - 结果</h2>
        <button className="download-btn" onClick={handleDownload}>⬇ 下载</button>
      </header>

      {error && <div className="error-msg">{error}</div>}

      <div className="compare-view">
        <div className="compare-container">
          <img
            src={uploadPreview}
            alt="原图"
            className="compare-img base"
          />
          <div
            className="compare-img overlay"
            style={{ clipPath: `inset(0 ${100 - comparePosition}% 0 0)` }}
          >
            <img src={resultUrl} alt="结果" />
          </div>
          <div
            className="compare-divider"
            style={{ left: `${comparePosition}%` }}
          >
            <div className="divider-handle" />
          </div>
        </div>
        <input
          type="range"
          className="compare-slider"
          min="0"
          max="100"
          value={comparePosition}
          onChange={(e) => setComparePosition(Number(e.target.value))}
        />
      </div>

      <div className="result-actions">
        <button className="action-btn secondary" onClick={() => setStep('upload')}>
          重新编辑
        </button>
        <button className="action-btn" onClick={handleDownload}>
          📥 下载结果
        </button>
      </div>
    </div>
  )
}
