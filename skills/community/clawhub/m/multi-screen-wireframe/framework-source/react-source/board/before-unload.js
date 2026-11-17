export const UNSAVED_REVIEW_MESSAGE = '修改内容尚未保存，离开页面后会丢失。是否继续？'

export function preventUnsavedReviewExit(event, message = UNSAVED_REVIEW_MESSAGE) {
  event.preventDefault()
  event.returnValue = message
  return message
}
