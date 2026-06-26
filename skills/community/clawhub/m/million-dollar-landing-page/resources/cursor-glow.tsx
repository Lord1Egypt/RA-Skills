'use client'

import { useEffect, useRef } from 'react'

interface CursorGlowProps {
  /**
   * The glow color as a CSS rgba string.
   * Use your brand accent at very low opacity (0.04–0.07).
   * Example: 'rgba(99,102,241,0.05)' for indigo, 'rgba(249,115,22,0.05)' for orange
   */
  color?: string
}

export function CursorGlow({ color = 'rgba(255,255,255,0.04)' }: CursorGlowProps) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let rafId: number

    const onMove = (e: MouseEvent) => {
      rafId = requestAnimationFrame(() => {
        if (!ref.current) return
        ref.current.style.background = `radial-gradient(700px circle at ${e.clientX}px ${e.clientY}px, ${color} 0%, transparent 55%)`
      })
    }

    window.addEventListener('mousemove', onMove, { passive: true })
    return () => {
      window.removeEventListener('mousemove', onMove)
      cancelAnimationFrame(rafId)
    }
  }, [color])

  return (
    <div
      ref={ref}
      className="fixed inset-0 pointer-events-none z-30"
      aria-hidden="true"
    />
  )
}
