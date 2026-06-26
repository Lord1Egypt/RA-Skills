import { createRouter, createWebHistory } from 'vue-router'

// 页面组件由 skill 生成时替换
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('../views/PlaceholderPage.vue') },
  ],
})

export default router
