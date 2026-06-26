import { createServerClient } from '@/lib/supabase/server'
import { registry } from '@/lib/registry'
import Link from 'next/link'
import { format } from 'date-fns'

export const metadata = { title: 'Dashboard | NormieClaw' }

function getTimeOfDay(): string {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
}

export default async function HomePage() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  const { data: profile } = await supabase
    .from('profiles')
    .select('display_name')
    .eq('id', user!.id)
    .single()

  const skills = registry.getEnabledSkills()

  return (
    <div className="space-y-8">
      {/* Greeting */}
      <div>
        <h1 className="text-[2rem] font-bold leading-tight text-text-1">
          Good {getTimeOfDay()}, {profile?.display_name || 'there'}
        </h1>
        <p className="text-[13px] text-text-3 mt-1">
          {format(new Date(), 'EEEE, MMMM d, yyyy')}
        </p>
      </div>

      {/* Quick Actions */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {skills.slice(0, 6).map((skill) => (
          <Link
            key={skill.id}
            href={skill.nav.defaultRoute}
            className="flex items-center gap-2 rounded-lg border border-border-soft bg-surface-1 px-4 py-2 hover:border-border-strong hover:bg-surface-2 transition-all whitespace-nowrap text-sm text-text-2"
          >
            <span>{skill.icon}</span>
            <span>{skill.nav.label}</span>
          </Link>
        ))}
      </div>

      {/* Widget Grid */}
      {skills.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {skills.map((skill) =>
            skill.homeWidgets.map((widget) => (
              <div
                key={`${skill.id}-${widget.id}`}
                className={
                  widget.span === 3
                    ? 'col-span-1 sm:col-span-2 lg:col-span-3'
                    : widget.span === 2
                    ? 'col-span-1 sm:col-span-2'
                    : 'col-span-1'
                }
              >
                {/* Widget placeholder — replace with actual widget component imports */}
                <div className="rounded-lg border border-border-soft bg-surface-1 p-6 noise-overlay">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{skill.icon}</span>
                    <h3 className="text-sm font-semibold text-text-1">{widget.component.replace(/([A-Z])/g, ' $1').trim()}</h3>
                  </div>
                  <p className="text-xs text-text-3">
                    Widget from {skill.displayName}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="rounded-lg border border-border-soft bg-surface-1 p-12 text-center noise-overlay">
          <div className="text-4xl mb-4">🚀</div>
          <h2 className="text-xl font-semibold text-text-1 mb-2">Welcome to NormieClaw</h2>
          <p className="text-sm text-text-3 max-w-md mx-auto">
            Install your first skill to get started. Each skill adds a page to your sidebar and widgets to this overview.
          </p>
        </div>
      )}

      {/* Recent Activity placeholder */}
      <section>
        <h2 className="text-lg font-semibold text-text-1 mb-4">Recent Activity</h2>
        <div className="rounded-lg border border-border-soft bg-surface-1 p-6 noise-overlay">
          <p className="text-sm text-text-3">Activity from your installed skills will appear here.</p>
        </div>
      </section>
    </div>
  )
}
