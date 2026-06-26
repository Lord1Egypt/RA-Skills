'use client'

import { cn } from '@/lib/utils/cn'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface StatCardProps {
  value: string | number
  label: string
  trend?: number
  trendLabel?: string
  icon?: React.ReactNode
  color?: 'teal' | 'orange' | 'blue' | 'green' | 'red' | 'yellow'
  onClick?: () => void
  className?: string
}

const colorMap: Record<string, { text: string; bg: string; border: string }> = {
  teal: {
    text: 'text-teal-400',
    bg: 'bg-teal-500/10',
    border: 'border-teal-500/20',
  },
  orange: {
    text: 'text-orange-400',
    bg: 'bg-orange-500/10',
    border: 'border-orange-500/20',
  },
  blue: {
    text: 'text-blue-400',
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/20',
  },
  green: {
    text: 'text-green-400',
    bg: 'bg-green-500/10',
    border: 'border-green-500/20',
  },
  red: {
    text: 'text-red-400',
    bg: 'bg-red-500/10',
    border: 'border-red-500/20',
  },
  yellow: {
    text: 'text-yellow-400',
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/20',
  },
}

export function StatCard({
  value,
  label,
  trend,
  trendLabel,
  icon,
  color = 'teal',
  onClick,
  className,
}: StatCardProps) {
  const colors = colorMap[color] ?? colorMap.teal

  return (
    <div
      onClick={onClick}
      className={cn(
        'rounded-lg border border-border-soft bg-surface-1 p-5 noise-overlay',
        'transition-all duration-200',
        onClick && 'cursor-pointer hover:border-border-strong hover:bg-surface-2',
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-[13px] text-text-3 font-medium">{label}</p>
          <p className="text-2xl font-bold text-text-1">{value}</p>
        </div>
        {icon && (
          <div className={cn('rounded-md p-2', colors.bg, colors.border, 'border')}>
            <span className={colors.text}>{icon}</span>
          </div>
        )}
      </div>

      {trend !== undefined && (
        <div className="mt-3 flex items-center gap-1.5">
          {trend > 0 ? (
            <TrendingUp size={14} className="text-green-400" />
          ) : trend < 0 ? (
            <TrendingDown size={14} className="text-red-400" />
          ) : (
            <Minus size={14} className="text-text-3" />
          )}
          <span
            className={cn(
              'text-xs font-medium',
              trend > 0 ? 'text-green-400' : trend < 0 ? 'text-red-400' : 'text-text-3'
            )}
          >
            {trend > 0 ? '+' : ''}
            {trend.toFixed(1)}%
          </span>
          {trendLabel && (
            <span className="text-xs text-text-3">{trendLabel}</span>
          )}
        </div>
      )}
    </div>
  )
}
