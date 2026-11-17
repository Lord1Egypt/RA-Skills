/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('login', ({ ref }) => ({
  setup() { return { phone: ref(''), code: ref('') } },
  template: /*html*/ `<WfColumn id="login-page" :gap="20" class="weekend-login login__page"><span id="login-logo" class="weekend-logo-placeholder login__logo" aria-hidden="true"></span><WfColumn class="login__intro" :gap="8"><WfHeading id="login-title" class="login__title" :level="1">周末出发</WfHeading><WfText class="login__description">把想去的地方，变成一份随时能走的行程。</WfText></WfColumn><WfFormField class="login__phone-field" label="手机号" for="login-phone"><WfTextInput id="login-phone" v-model="phone" class="login__phone-input" inputmode="tel" placeholder="请输入手机号" /></WfFormField><WfFormField class="login__code-field" label="验证码" for="login-code" hint="演示环境可输入任意 6 位数字"><WfTextInput id="login-code" v-model="code" class="login__code-input" inputmode="numeric" placeholder="请输入验证码" /></WfFormField><WfButton id="login-submit" class="login__submit" variant="primary" to="discover">开始探索</WfButton><WfText class="login__agreement" as="small">继续即表示同意服务条款与隐私说明。</WfText></WfColumn>`,
}))
