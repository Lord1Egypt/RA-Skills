import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  const authEnabled = await authStore.checkAuthConfig()

  if (!authEnabled) {
    if (to.name === 'Login') {
      next({ name: 'Dashboard' })
      return
    }
    next()
    return
  }

  if (to.meta.public) {
    if (to.name === 'Login' && authStore.isAuthenticated) {
      const valid = await authStore.checkAuth()
      if (valid) {
        const redirect = typeof to.query.redirect === 'string' ? to.query.redirect : '/'
        next(redirect)
        return
      }
    }
    next()
    return
  }

  if (!authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  const valid = await authStore.checkAuth()
  if (!valid) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  next()
})

export default router
