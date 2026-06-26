import './globals.css'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: '马上有福 🐴 AI专属马年祝福',
  description: '输入你的名字，AI为你写一首专属马年祝福',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen">{children}</body>
    </html>
  )
}
