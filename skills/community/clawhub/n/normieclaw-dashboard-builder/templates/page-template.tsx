import { createServerClient } from '@/lib/supabase/server'

/**
 * Page Template — Skeleton for a skill page.
 *
 * Usage: Copy this file, rename, and customize for your skill.
 * Replace SKILL_NAME, TABLE_NAME, and column definitions.
 *
 * This is a React Server Component — no 'use client' needed.
 * Data fetching happens at the server level with full RLS protection.
 */

interface PageHeaderProps {
  title: string
  description?: string
  actions?: React.ReactNode
}

function PageHeader({ title, description, actions }: PageHeaderProps) {
  return (
    <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 className="text-[1.75rem] font-bold text-text-1">{title}</h1>
        {description && (
          <p className="text-[13px] text-text-3 mt-0.5">{description}</p>
        )}
      </div>
      {actions && <div className="flex gap-2 mt-2 sm:mt-0">{actions}</div>}
    </div>
  )
}

export default async function SkillPage() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) return null

  // ── Replace with your skill's data query ──
  // const { data, error } = await supabase
  //   .from('prefix_table')
  //   .select('*')
  //   .eq('user_id', user.id)
  //   .order('created_at', { ascending: false })

  return (
    <div className="space-y-8">
      <PageHeader
        title="SKILL_NAME"
        description="Brief description of what this page shows"
        actions={
          <button className="rounded-md bg-teal-500 px-4 py-2 text-sm font-semibold text-bg-950 hover:bg-teal-400 transition-colors">
            Add Item
          </button>
        }
      />

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* Import and use StatCard components here */}
      </div>

      {/* Main content */}
      <div className="rounded-lg border border-border-soft bg-surface-1 p-6 noise-overlay">
        {/* Import and use DataTable, ChartWrapper, or custom components here */}
        <p className="text-sm text-text-3">Content goes here</p>
      </div>
    </div>
  )
}
