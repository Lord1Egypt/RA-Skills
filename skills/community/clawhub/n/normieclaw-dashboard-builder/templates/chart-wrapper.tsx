'use client'

import {
  LineChart, Line,
  BarChart, Bar,
  PieChart, Pie, Cell,
  CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { cn } from '@/lib/utils/cn'

interface Series {
  key: string
  label: string
  color: string
}

interface ChartWrapperProps {
  type: 'line' | 'bar' | 'donut'
  data: Record<string, any>[]
  xKey: string
  series: Series[]
  height?: number
  showGrid?: boolean
  showLegend?: boolean
  className?: string
}

const tooltipStyle = {
  backgroundColor: 'var(--bg-850)',
  border: '1px solid var(--border-strong)',
  borderRadius: '8px',
  color: 'var(--text-1)',
  fontSize: '12px',
  padding: '8px 12px',
}

const axisStyle = {
  fontSize: 11,
  fill: 'var(--text-3)',
  fontFamily: 'Manrope, sans-serif',
}

export function ChartWrapper({
  type,
  data,
  xKey,
  series,
  height = 300,
  showGrid = true,
  showLegend = true,
  className,
}: ChartWrapperProps) {
  if (!data || data.length === 0) {
    return (
      <div
        className={cn('flex items-center justify-center rounded-lg border border-border-soft bg-surface-1', className)}
        style={{ height }}
      >
        <p className="text-sm text-text-3">No chart data yet</p>
      </div>
    )
  }

  const renderChart = () => {
    switch (type) {
      case 'line':
        return (
          <LineChart data={data}>
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-soft)" />
            )}
            <XAxis dataKey={xKey} tick={axisStyle} axisLine={false} tickLine={false} />
            <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            {showLegend && <Legend wrapperStyle={{ fontSize: 12 }} />}
            {series.map((s) => (
              <Line
                key={s.key}
                type="monotone"
                dataKey={s.key}
                name={s.label}
                stroke={s.color}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, strokeWidth: 0, fill: s.color }}
              />
            ))}
          </LineChart>
        )

      case 'bar':
        return (
          <BarChart data={data}>
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-soft)" />
            )}
            <XAxis dataKey={xKey} tick={axisStyle} axisLine={false} tickLine={false} />
            <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            {showLegend && <Legend wrapperStyle={{ fontSize: 12 }} />}
            {series.map((s) => (
              <Bar
                key={s.key}
                dataKey={s.key}
                name={s.label}
                fill={s.color}
                radius={[4, 4, 0, 0]}
              />
            ))}
          </BarChart>
        )

      case 'donut':
        return (
          <PieChart>
            <Pie
              data={data}
              dataKey={series[0]?.key ?? 'value'}
              nameKey={xKey}
              cx="50%"
              cy="50%"
              innerRadius="55%"
              outerRadius="80%"
              paddingAngle={2}
              stroke="none"
            >
              {data.map((_, i) => (
                <Cell key={i} fill={series[i % series.length]?.color ?? '#14b8a6'} />
              ))}
            </Pie>
            <Tooltip contentStyle={tooltipStyle} />
            {showLegend && <Legend wrapperStyle={{ fontSize: 12 }} />}
          </PieChart>
        )
    }
  }

  return (
    <div className={cn('rounded-lg border border-border-soft bg-surface-1 p-4 noise-overlay', className)}>
      <ResponsiveContainer width="100%" height={height}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  )
}
