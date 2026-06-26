'use client'

import { useEffect, useRef } from 'react'

export function ScrollProgress() {
  const barRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const update = () => {
      const scrollTop = window.scrollY
      const docHeight = document.documentElement.scrollHeight - window.innerHeight
      const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0
      if (barRef.current) barRef.current.style.height = `${pct}%`
    }
    window.addEventListener('scroll', update, { passive: true })
    update()
    return () => window.removeEventListener('scroll', update)
  }, [])

  return (
    <div className="fixed right-0 top-0 h-full w-[2px] z-50 pointer-events-none bg-white/[0.04]">
      <div ref={barRef} className="bg-orange-500 w-full transition-none" style={{ height: '0%' }} />
    </div>
  )
}
