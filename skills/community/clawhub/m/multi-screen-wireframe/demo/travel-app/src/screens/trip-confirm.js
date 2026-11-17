/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('trip-confirm', ({ onUnmounted, ref }) => ({
  setup() {
    const confirmOpen = ref(false)
    const loading = ref(false)
    const saved = ref(false)
    let timer = 0
    const submitTrip = () => {
      confirmOpen.value = false
      loading.value = true
      window.clearTimeout(timer)
      timer = window.setTimeout(() => { loading.value = false; saved.value = true }, 700)
    }
    onUnmounted(() => window.clearTimeout(timer))
    return { confirmOpen, loading, saved, submitTrip, steps: [{ id: 'basic', label: '基本信息' }, { id: 'budget', label: '预算' }, { id: 'confirm', label: '确认' }] }
  },
  template: /*html*/ `<WfMobileLayout><WfColumn id="trip-confirm-page" :gap="18" class="weekend-page trip-confirm__page"><WfPageHeader id="trip-confirm-header" title-id="trip-confirm-title" class="trip-confirm__header" title="确认行程" subtitle="检查信息后保存到我的行程" /><WfSteps id="trip-confirm-steps" class="trip-confirm__steps" :current="2" :items="steps" /><WfCard id="trip-confirm-summary" class="trip-confirm__summary"><WfColumn class="trip-confirm__summary-body" :gap="10"><WfRow class="trip-confirm__summary-heading" align-items="center" justify-content="space-between" :gap="8"><strong class="trip-confirm__trip-name">周六运河散步</strong><WfBadge class="trip-confirm__status">待保存</WfBadge></WfRow><WfText class="trip-confirm__date">2026 年 8 月 15 日 · 周六</WfText><WfText class="trip-confirm__route">运河边的一天 · 8.6 km · 约 6 小时</WfText></WfColumn></WfCard><WfColumn id="trip-confirm-details" class="trip-confirm__details" :gap="0"><WfCell class="trip-confirm__detail" title="集合地点" subtitle="运河路地铁站 3 号口" /><WfCell class="trip-confirm__detail" title="行程节奏" value="轻松" /><WfCell class="trip-confirm__detail" title="同行人数" value="3 人" /><WfCell class="trip-confirm__detail" title="出发提醒" value="已开启" /></WfColumn><WfCard id="trip-confirm-budget" class="trip-confirm__budget" to="budget"><WfRow class="trip-confirm__budget-body" align-items="center" justify-content="space-between"><WfColumn class="trip-confirm__budget-copy" :gap="5"><WfText class="trip-confirm__budget-label">预计总费用</WfText><WfText class="trip-confirm__budget-note">查看明细与同行人</WfText></WfColumn><span class="trip-confirm__total">428 元</span></WfRow></WfCard><WfColumn id="trip-confirm-actions" class="trip-confirm__actions" :gap="10"><WfButton id="trip-confirm-submit" class="trip-confirm__submit" variant="primary" @click="confirmOpen = true">确认并保存</WfButton><WfButton class="trip-confirm__trips-action" to="trips">查看我的行程</WfButton></WfColumn><WfConfirmDialog id="trip-confirm-dialog" class="trip-confirm__dialog" :open="confirmOpen" title="保存这份行程？" message="保存后会同步给已加入的同行人，并在出发前发送提醒。" confirm-label="确认保存" @confirm="submitTrip" @cancel="confirmOpen = false" /><WfLoadingOverlay id="trip-confirm-loading" class="trip-confirm__loading" :open="loading" label="正在生成行程" /><WfToast id="trip-confirm-toast" class="trip-confirm__toast" :open="saved">行程已保存，可在“我的行程”查看。</WfToast></WfColumn></WfMobileLayout>`,
}))
