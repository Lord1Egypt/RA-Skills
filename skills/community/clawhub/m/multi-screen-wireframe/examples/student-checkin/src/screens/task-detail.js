/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('task-detail', ({ ref, computed, onUnmounted }) => ({
  setup() {
    const samples = {
      homework: {
        id: 'hw-math',
        title: '数学口算打卡',
        type: 'homework',
        subject: '数学',
        meta: '两位数加减 · 20 题',
        note: '独立完成口算卡，家长可抽查订正。完成后点「完成打卡」。',
      },
      habit: {
        id: 'hb-read',
        title: '阅读打卡',
        type: 'habit',
        subject: '习惯',
        meta: '不少于 20 分钟',
        note: '阅读课外书或课文扩展。提交前需添加凭证占位（照片或录音）。',
      },
    }

    const sampleKey = ref('homework')
    const evidenceAdded = ref(false)
    const toastOpen = ref(false)
    const toastLabel = ref('请先添加凭证')
    let toastTimer = null

    const activeTask = computed(() => samples[sampleKey.value])
    const isHabit = computed(() => activeTask.value.type === 'habit')

    const sampleTabs = [
      { id: 'homework', label: '作业样例' },
      { id: 'habit', label: '习惯样例' },
    ]

    function onSampleChange(id) {
      sampleKey.value = id
      evidenceAdded.value = false
      toastOpen.value = false
    }

    function addEvidence() {
      evidenceAdded.value = true
    }

    function showToast(label) {
      toastLabel.value = label
      toastOpen.value = true
      if (toastTimer) clearTimeout(toastTimer)
      toastTimer = setTimeout(() => {
        toastOpen.value = false
        toastTimer = null
      }, 2000)
    }

    function submitHabit() {
      if (!evidenceAdded.value) {
        showToast('请先添加凭证')
      }
    }

    onUnmounted(() => {
      if (toastTimer) clearTimeout(toastTimer)
    })

    return {
      sampleKey,
      sampleTabs,
      activeTask,
      isHabit,
      evidenceAdded,
      toastOpen,
      toastLabel,
      onSampleChange,
      addEvidence,
      submitHabit,
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="task-detail-page" class="checkin-page task-detail__page" :gap="18">
        <WfPageHeader
          id="task-detail-header"
          title-id="task-detail-title"
          subtitle-id="task-detail-subtitle"
          class="task-detail__header"
          title="任务详情"
          subtitle="按任务类型演示两种打卡方式"
        >
          <template #actions>
            <WfButton id="task-detail-back" class="task-detail__back" to="today">返回</WfButton>
          </template>
        </WfPageHeader>

        <WfTabs
          id="task-detail-samples"
          class="task-detail__samples"
          :items="sampleTabs"
          :active-id="sampleKey"
          @update:active-id="onSampleChange"
        />

        <WfCard id="task-detail-card" class="task-detail__card">
          <WfColumn class="task-detail__body" :gap="12">
            <WfRow class="task-detail__badges" :gap="8">
              <WfBadge class="task-detail__badge">{{ activeTask.subject }}</WfBadge>
              <WfBadge class="task-detail__badge">{{ isHabit ? '习惯' : '作业' }}</WfBadge>
            </WfRow>
            <WfHeading id="task-detail-name" class="task-detail__name" :level="2">{{ activeTask.title }}</WfHeading>
            <WfText class="task-detail__meta">{{ activeTask.meta }}</WfText>
            <WfText class="task-detail__note">{{ activeTask.note }}</WfText>
          </WfColumn>
        </WfCard>

        <WfColumn v-if="isHabit" id="task-detail-evidence" class="task-detail__evidence" :gap="12">
          <WfHeading id="taREDACTED-SECRET" class="checkin-section-heading" :level="3">打卡凭证</WfHeading>
          <WfCard id="taREDACTED-SECRET" class="taREDACTED-SECRET">
            <WfColumn class="taREDACTED-SECRET" :gap="10">
              <WfImagePlaceholder
                id="taREDACTED-SECRET"
                class="taREDACTED-SECRET"
                :height="140"
                :border-radius="0"
              />
              <WfText class="taREDACTED-SECRET">
                {{ evidenceAdded ? '已添加凭证占位' : '尚未添加凭证' }}
              </WfText>
              <WfButton
                id="task-detail-add-evidence"
                class="taREDACTED-SECRET"
                :variant="evidenceAdded ? 'default' : 'primary'"
                @click="addEvidence"
              >
                {{ evidenceAdded ? '已添加凭证' : '添加凭证' }}
              </WfButton>
            </WfColumn>
          </WfCard>
        </WfColumn>

        <WfRow id="task-detail-actions" class="task-detail__actions" :gap="10">
          <WfButton
            v-if="!isHabit"
            id="taREDACTED-SECRET"
            class="task-detail__complete"
            variant="primary"
            to="checkin-result"
          >
            完成打卡
          </WfButton>
          <WfButton
            v-else
            id="task-detail-submit-habit"
            class="task-detail__submit"
            variant="primary"
            :to="evidenceAdded ? 'checkin-result' : ''"
            @click="submitHabit"
          >
            提交打卡
          </WfButton>
        </WfRow>

        <WfToast :open="toastOpen" :label="toastLabel" />
      </WfColumn>
    </WfMobileLayout>
  `,
}))
