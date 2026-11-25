export interface FrameSpec {
  /** 帧 id，只用于标识 */
  id: string
  /** 缩略图与目录里显示的名字 */
  name: string
  /** 帧内容，一段静态 HTML */
  html: string
}

export interface MorphOptions {
  duration?: number
  ease?: string
}
