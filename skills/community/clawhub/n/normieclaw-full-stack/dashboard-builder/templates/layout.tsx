import { Manrope, JetBrains_Mono } from 'next/font/google'
import { Sidebar } from '@/components/shell/sidebar'
import { Header } from '@/components/shell/header'
import { createServerClient } from '@/lib/supabase/server'
import { registry } from '@/lib/registry'
import '@/styles/globals.css'

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata = {
  title: 'NormieClaw Dashboard',
  description: 'Your unified AI skill dashboard',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return (
      <html lang="en" className="dark">
        <body className={`${manrope.variable} ${jetbrainsMono.variable} font-sans bg-bg-950 text-text-1`}>
          {children}
        </body>
      </html>
    )
  }

  const skills = registry.getEnabledSkills()

  return (
    <html lang="en" className="dark">
      <body className={`${manrope.variable} ${jetbrainsMono.variable} font-sans bg-bg-950 text-text-1`}>
        <div className="flex h-screen overflow-hidden">
          {/* Sidebar — hidden on mobile */}
          <Sidebar skills={skills} className="hidden md:flex" />

          {/* Main content area */}
          <div className="flex flex-1 flex-col overflow-hidden">
            <Header user={user} />
            <main className="flex-1 overflow-y-auto bg-bg-900 p-6">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
