import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import ArcoVueIcon from '@arco-design/web-vue/es/icon'
import '@arco-design/web-vue/dist/arco.css'
import '@arco-themes/vue-pangea-3-linear/index.less'
import router from './router'
import App from './App.vue'

const app = createApp(App)
app.use(ArcoVue)
app.use(ArcoVueIcon)
app.use(router)
app.mount('#app')
