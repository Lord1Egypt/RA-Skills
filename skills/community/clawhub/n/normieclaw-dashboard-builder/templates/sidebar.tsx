'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ChevronLeft, ChevronRight, ChevronDown, Settings, Home, Bell } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import * as LucideIcons from 'lucide-react'
import type { SkillManifest } from '@/lib/types/skill'

interface SidebarProps {
  skills: SkillManifest[]
  className?: string
}

function SkillIcon({ name, size = 20 }: { name: string; size?: number }) {
  const Icon = (LucideIcons as Record<string, any>)[name]
  if (!Icon) return <span className="text-sm">●</span>
  return <Icon size={size} />
}

const CATEGORY_ORDER: Record<string, number> = {
  finance: 1, productivity: 2, work: 3, health: 4, learning: 5, lifestyle: 6,
}
const CATEGORY_LABELS: Record<string, string> = {
  finance: 'Finance', productivity: 'Productivity', work: 'Work',
  health: 'Health & Wellness', learning: 'Learning', lifestyle: 'Lifestyle',
}

export function Sidebar({ skills, className }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)
  const [expandedSkill, setExpandedSkill] = useState<string | null>(null)
  const pathname = usePathname()

  // Group skills by category
  const groups: Record<string, SkillManifest[]> = {}
  for (const skill of skills) {
    const cat = skill.category || 'other'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(skill)
  }
  const sortedGroups = Object.entries(groups)
    .sort(([a], [b]) => (CATEGORY_ORDER[a] ?? 99) - (CATEGORY_ORDER[b] ?? 99))

  return (
    <aside
      className={cn(
        'flex flex-col border-r border-border-soft bg-bg-850 noise-overlay',
        'transition-all duration-300 ease-in-out',
        collapsed ? 'w-[68px]' : 'w-[260px]',
        className
      )}
    >
      {/* Logo */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border-soft">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2">
            <img src="/logo.svg" alt="NormieClaw" className="h-8 w-8" />
            <span className="text-lg font-semibold text-text-1">NormieClaw</span>
          </Link>
        )}
        {collapsed && (
          <Link href="/" className="mx-auto">
            <img src="/logo.svg" alt="NormieClaw" className="h-8 w-8" />
          </Link>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-md hover:bg-surface-2 text-text-3 hover:text-text-1 transition-colors"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-2 px-2">
        {/* Home */}
        <NavItem href="/" icon={<Home size={20} />} label="Dashboard" active={pathname === '/'} collapsed={collapsed} />
        {/* Notifications */}
        <NavItem href="/notifications" icon={<Bell size={20} />} label="Notifications" active={pathname === '/notifications'} collapsed={collapsed} />

        {/* Skill groups */}
        {sortedGroups.map(([category, categorySkills]) => (
          <div key={category} className="mt-4">
            {!collapsed && (
              <p className="px-3 mb-1 text-[11px] font-medium uppercase tracking-wider text-text-3">
                {CATEGORY_LABELS[category] ?? category}
              </p>
            )}
            {collapsed && <div className="my-2 mx-3 h-px bg-border-soft" />}

            {categorySkills.map((skill) => {
              const isActive = pathname.startsWith(skill.nav.defaultRoute)
              const hasChildren = skill.nav.children && skill.nav.children.length > 0
              const isExpanded = expandedSkill === skill.id

              return (
                <div key={skill.id}>
                  <div className="flex items-center">
                    <Link
                      href={skill.nav.defaultRoute}
                      className={cn(
                        'flex flex-1 items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
                        isActive
                          ? 'bg-surface-3 text-teal-400 border-l-2 border-l-teal-500'
                          : 'text-text-2 hover:bg-surface-2 hover:text-text-1'
                      )}
                    >
                      <SkillIcon name={skill.lucideIcon} size={20} />
                      {!collapsed && <span className="truncate">{skill.nav.label}</span>}
                    </Link>
                    {hasChildren && !collapsed && (
                      <button
                        onClick={() => setExpandedSkill(isExpanded ? null : skill.id)}
                        className="p-1 mr-1 rounded hover:bg-surface-2 text-text-3"
                      >
                        <ChevronDown size={14} className={cn('transition-transform', isExpanded && 'rotate-180')} />
                      </button>
                    )}
                  </div>
                  {/* Sub-items */}
                  {hasChildren && isExpanded && !collapsed && (
                    <div className="ml-9 mt-0.5 space-y-0.5">
                      {skill.nav.children!.map((child) => (
                        <Link
                          key={child.route}
                          href={child.route}
                          className={cn(
                            'block rounded-md px-3 py-1.5 text-[13px] transition-colors',
                            pathname === child.route
                              ? 'text-teal-400 bg-surface-2'
                              : 'text-text-3 hover:text-text-2 hover:bg-surface-2'
                          )}
                        >
                          {child.label}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-border-soft p-2">
        <NavItem href="/settings" icon={<Settings size={20} />} label="Settings" active={pathname.startsWith('/settings')} collapsed={collapsed} />
      </div>
    </aside>
  )
}

function NavItem({ href, icon, label, active, collapsed }: {
  href: string; icon: React.ReactNode; label: string; active: boolean; collapsed: boolean
}) {
  return (
    <Link
      href={href}
      className={cn(
        'flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
        active
          ? 'bg-surface-3 text-teal-400'
          : 'text-text-2 hover:bg-surface-2 hover:text-text-1'
      )}
      title={collapsed ? label : undefined}
    >
      {icon}
      {!collapsed && <span>{label}</span>}
    </Link>
  )
}
