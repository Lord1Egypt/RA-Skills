(function initWireframeVueUi(global) {
  'use strict'

  const Vue = global.Vue
  const Wireframe = global.WireframeVue
  if (!Vue || !Wireframe) throw new Error('Vue and WireframeVue are required before ui.js')

  const { Teleport, computed, defineComponent, h, inject, mergeProps, onMounted, ref } = Vue

  function classes(...values) {
    return values.flat().filter(Boolean)
  }

  function content(slots, name = 'default') {
    return slots[name] ? slots[name]() : []
  }

  function withBase(attrs, base, extra) {
    return mergeProps(attrs, { class: classes(base, extra) })
  }

  function withFlow(attrs, to, base, extra) {
    return mergeProps(attrs, {
      class: classes(base, to && 'wf-interactive', extra),
      role: to ? 'link' : attrs.role,
      tabindex: to && attrs.tabindex == null ? 0 : attrs.tabindex,
      'data-flow-to': to || undefined,
    })
  }

  function layoutComponent(name, baseClass, direction) {
    return defineComponent({
      name,
      inheritAttrs: false,
      props: {
        gap: { type: [Number, String], default: 0 },
        alignItems: { type: String, default: 'stretch' },
        justifyContent: { type: String, default: 'flex-start' },
        to: { type: String, default: '' },
      },
      setup(props, { attrs, slots }) {
        return () => h('div', withFlow(attrs, props.to, baseClass, null), content(slots))
      },
    })
  }

  const WfBox = defineComponent({
    name: 'WfBox',
    inheritAttrs: false,
    props: { to: { type: String, default: '' } },
    setup(props, { attrs, slots }) {
      return () => h('div', withFlow(attrs, props.to, 'wf-box', null), content(slots))
    },
  })

  function flexLayout(name, baseClass, direction) {
    return defineComponent({
      name,
      inheritAttrs: false,
      props: {
        gap: { type: [Number, String], default: 0 },
        alignItems: { type: String, default: 'stretch' },
        justifyContent: { type: String, default: 'flex-start' },
        to: { type: String, default: '' },
      },
      setup(props, { attrs, slots }) {
        return () => h('div', mergeProps(withFlow(attrs, props.to, baseClass, null), {
          style: {
            display: 'flex',
            flexDirection: direction,
            gap: typeof props.gap === 'number' ? `${props.gap}px` : props.gap,
            alignItems: props.alignItems,
            justifyContent: props.justifyContent,
          },
        }), content(slots))
      },
    })
  }

  const WfRow = flexLayout('WfRow', 'wf-row', 'row')
  const WfColumn = flexLayout('WfColumn', 'wf-column', 'column')

  const WfGrid = defineComponent({
    name: 'WfGrid',
    inheritAttrs: false,
    props: {
      columns: { type: [Number, String, Object], default: 1 },
      gap: { type: [Number, String], default: 0 },
      to: { type: String, default: '' },
    },
    setup(props, { attrs, slots }) {
      const viewportKey = inject(Wireframe.keys.viewportKey, ref(''))
      const gridTemplateColumns = computed(() => {
        const candidate = props.columns && typeof props.columns === 'object'
          ? props.columns[viewportKey.value]
          : props.columns
        if (Number.isInteger(candidate) && candidate > 0) {
          return `repeat(${candidate}, minmax(0, 1fr))`
        }
        if (typeof candidate === 'string' && candidate.trim()) return candidate
        throw new Error('WfGrid columns must resolve to a positive integer or CSS string')
      })
      return () => h('div', mergeProps(withFlow(attrs, props.to, 'wf-grid', null), {
        style: {
          display: 'grid',
          gridTemplateColumns: gridTemplateColumns.value,
          gap: typeof props.gap === 'number' ? `${props.gap}px` : props.gap,
        },
      }), content(slots))
    },
  })

  const WfHeading = defineComponent({
    name: 'WfHeading',
    inheritAttrs: false,
    props: { level: { type: Number, default: 2 } },
    setup(props, { attrs, slots }) {
      return () => h(`h${Math.min(6, Math.max(1, props.level))}`, withBase(attrs, 'wf-heading'), content(slots))
    },
  })

  const WfText = defineComponent({
    name: 'WfText',
    inheritAttrs: false,
    props: { as: { type: String, default: 'p' } },
    setup(props, { attrs, slots }) {
      return () => h(props.as, withBase(attrs, 'wf-text'), content(slots))
    },
  })

  const WfCard = defineComponent({
    name: 'WfCard',
    inheritAttrs: false,
    props: { to: { type: String, default: '' } },
    setup(props, { attrs, slots }) {
      return () => h('div', withFlow(attrs, props.to, 'wf-card'), content(slots))
    },
  })

  const WfBadge = defineComponent({
    name: 'WfBadge',
    inheritAttrs: false,
    setup(_props, { attrs, slots }) {
      return () => h('span', withBase(attrs, 'wf-badge'), content(slots))
    },
  })

  const WfAvatar = defineComponent({
    name: 'WfAvatar',
    inheritAttrs: false,
    props: {
      size: { type: [Number, String], default: 40 },
      label: { type: String, default: '' },
    },
    setup(props, { attrs }) {
      return () => h('div', mergeProps(withBase(attrs, 'wf-avatar'), {
        'aria-label': props.label || undefined,
        style: {
          width: typeof props.size === 'number' ? `${props.size}px` : props.size,
          height: typeof props.size === 'number' ? `${props.size}px` : props.size,
        },
      }))
    },
  })

  const WfImagePlaceholder = defineComponent({
    name: 'WfImagePlaceholder',
    inheritAttrs: false,
    props: {
      width: { type: [Number, String], default: '100%' },
      height: { type: [Number, String], default: 160 },
      borderRadius: { type: [Number, String], default: 0 },
    },
    setup(props, { attrs }) {
      const cssValue = (value) => typeof value === 'number' ? `${value}px` : value
      return () => h('div', mergeProps(withBase(attrs, 'wf-image-placeholder'), {
        'aria-hidden': 'true',
        style: {
          width: cssValue(props.width),
          height: cssValue(props.height),
          borderRadius: cssValue(props.borderRadius),
        },
      }), [h('span', { class: 'wf-placeholder-block' })])
    },
  })

  const WfButton = defineComponent({
    name: 'WfButton',
    inheritAttrs: false,
    props: {
      to: { type: String, default: '' },
      variant: { type: String, default: 'default' },
    },
    setup(props, { attrs, slots }) {
      return () => h('button', mergeProps(withFlow(attrs, props.to, 'wf-button', `wf-button-${props.variant}`), {
        type: attrs.type || 'button',
      }), content(slots))
    },
  })

  function modelControl(name, tag, baseClass, eventName) {
    return defineComponent({
      name,
      inheritAttrs: false,
      props: { modelValue: { default: '' } },
      emits: ['update:modelValue'],
      setup(props, { attrs, emit, slots }) {
        const handler = (event) => emit('update:modelValue', event.target.value)
        return () => h(tag, mergeProps(withBase(attrs, baseClass), {
          value: props.modelValue,
          [eventName]: handler,
        }), content(slots))
      },
    })
  }

  const WfTextInput = modelControl('WfTextInput', 'input', 'wf-input', 'onInput')
  const WfTextArea = modelControl('WfTextArea', 'textarea', 'wf-input wf-textarea', 'onInput')
  const WfSelect = modelControl('WfSelect', 'select', 'wf-input wf-select', 'onChange')

  function choiceComponent(name, type) {
    return defineComponent({
      name,
      inheritAttrs: false,
      props: {
        label: { type: String, default: '' },
        modelValue: { type: Boolean, default: false },
      },
      emits: ['update:modelValue'],
      setup(props, { attrs, emit }) {
        return () => h('label', { class: classes('wf-choice', attrs.class) }, [
          h('input', mergeProps(attrs, {
            class: 'wf-choice-input',
            type,
            checked: props.modelValue,
            onChange: (event) => emit('update:modelValue', event.target.checked),
          })),
          h('span', { class: 'wf-choice-label' }, props.label),
        ])
      },
    })
  }

  const WfCheckbox = choiceComponent('WfCheckbox', 'checkbox')
  const WfRadio = choiceComponent('WfRadio', 'radio')

  const WfToggle = defineComponent({
    name: 'WfToggle',
    inheritAttrs: false,
    props: {
      checked: { type: Boolean, default: false },
      label: { type: String, default: '' },
    },
    emits: ['update:checked', 'change'],
    setup(props, { attrs, emit }) {
      return () => h('button', mergeProps(withBase(attrs, 'wf-toggle'), {
        type: 'button',
        role: 'switch',
        'aria-checked': String(props.checked),
        onClick: (event) => {
          emit('update:checked', !props.checked)
          emit('change', !props.checked, event)
        },
      }), [
        h('span', { class: 'wf-toggle-track' }, [h('span', { class: 'wf-toggle-thumb' })]),
        props.label ? h('span', { class: 'wf-toggle-label' }, props.label) : null,
      ])
    },
  })

  const WfFormField = defineComponent({
    name: 'WfFormField',
    inheritAttrs: false,
    props: {
      label: { type: String, default: '' },
      for: { type: String, default: '' },
      hint: { type: String, default: '' },
      error: { type: String, default: '' },
    },
    setup(props, { attrs, slots }) {
      return () => h('div', withBase(attrs, 'wf-form-field'), [
        h('label', { class: 'wf-field-label', for: props.for || undefined }, props.label),
        ...content(slots),
        props.hint && !props.error ? h('span', { class: 'wf-field-hint' }, props.hint) : null,
        props.error ? h('span', { class: 'wf-field-error', role: 'alert' }, props.error) : null,
      ])
    },
  })

  const WfPageHeader = defineComponent({
    name: 'WfPageHeader',
    inheritAttrs: false,
    props: {
      title: { type: String, default: '' },
      titleId: { type: String, default: '' },
      subtitle: { type: String, default: '' },
      subtitleId: { type: String, default: '' },
    },
    setup(props, { attrs, slots }) {
      return () => h('header', withBase(attrs, 'wf-page-header'), [
        h('div', { class: 'wf-page-header-copy' }, [
          h('h1', { id: props.titleId || undefined, class: 'wf-page-title' }, props.title),
          props.subtitle
            ? h('p', { id: props.subtitleId || undefined, class: 'wf-page-subtitle' }, props.subtitle)
            : null,
        ]),
        slots.actions ? h('div', { class: 'wf-page-actions' }, slots.actions()) : null,
      ])
    },
  })

  function navigationButtons(items, activeId, tabMode) {
    return items.map((item) => h('button', {
      type: 'button',
      key: item.to,
      class: classes(tabMode ? 'wf-tab-item' : 'wf-nav-item', item.to === activeId && 'is-active'),
      'data-flow-to': item.to,
      onClick: item.onClick,
    }, [
      h('span', { class: tabMode ? 'wf-tab-icon' : 'wf-nav-mark', 'aria-hidden': 'true' }),
      h('span', { class: tabMode ? 'wf-tab-label' : 'wf-nav-label' }, item.label),
    ]))
  }

  const WfSideNav = defineComponent({
    name: 'WfSideNav',
    inheritAttrs: false,
    props: {
      items: { type: Array, default: () => [] },
      activeId: { type: String, default: '' },
    },
    setup(props, { attrs }) {
      return () => h('nav', withBase(attrs, 'wf-side-nav'), navigationButtons(props.items, props.activeId, false))
    },
  })

  const WfTabBar = defineComponent({
    name: 'WfTabBar',
    inheritAttrs: false,
    props: {
      items: { type: Array, default: () => [] },
      activeId: { type: String, default: '' },
    },
    setup(props, { attrs }) {
      return () => h('nav', withBase(attrs, 'wf-tab-bar'), navigationButtons(props.items, props.activeId, true))
    },
  })

  const WfBreadcrumbs = defineComponent({
    name: 'WfBreadcrumbs',
    inheritAttrs: false,
    props: { items: { type: Array, default: () => [] } },
    setup(props, { attrs }) {
      return () => h('nav', mergeProps(withBase(attrs, 'wf-breadcrumbs'), { 'aria-label': 'Breadcrumbs' }),
        props.items.flatMap((item, index) => [
          index > 0 ? h('span', { class: 'wf-breadcrumb-divider', 'aria-hidden': 'true' }) : null,
          item.to
            ? h('button', { class: 'wf-breadcrumb-link', type: 'button', 'data-flow-to': item.to }, item.label)
            : h('span', { class: 'wf-breadcrumb-current' }, item.label),
        ]))
    },
  })

  const WfMobileShell = defineComponent({
    name: 'WfMobileShell',
    inheritAttrs: false,
    props: {
      tabs: { type: Array, default: () => [] },
      activeId: { type: String, default: '' },
    },
    setup(props, { attrs, slots }) {
      return () => h('div', withBase(attrs, 'wf-mobile-shell'), [
        h('main', { class: 'wf-mobile-shell-body' }, content(slots)),
        props.tabs.length ? h(WfTabBar, { items: props.tabs, activeId: props.activeId }) : null,
      ])
    },
  })

  const WfCell = defineComponent({
    name: 'WfCell',
    inheritAttrs: false,
    props: {
      to: { type: String, default: '' },
      title: { type: String, default: '' },
      subtitle: { type: String, default: '' },
      value: { default: undefined },
    },
    setup(props, { attrs, slots }) {
      return () => h('div', withFlow(attrs, props.to, 'wf-cell'), [
        h('div', { class: 'wf-cell-main' }, [
          h('strong', { class: 'wf-cell-title' }, props.title),
          props.subtitle ? h('span', { class: 'wf-cell-subtitle' }, props.subtitle) : null,
          ...content(slots),
        ]),
        props.value !== undefined ? h('span', { class: 'wf-cell-value' }, String(props.value)) : null,
      ])
    },
  })

  const WfDataTable = defineComponent({
    name: 'WfDataTable',
    inheritAttrs: false,
    props: {
      columns: { type: Array, default: () => [] },
      rows: { type: Array, default: () => [] },
      getRowKey: { type: Function, default: null },
    },
    setup(props, { attrs }) {
      return () => h('div', withBase(attrs, 'wf-table-wrap'), [
        h('table', { class: 'wf-table' }, [
          h('thead', { class: 'wf-table-head' }, [
            h('tr', { class: 'wf-table-header-row' }, props.columns.map((column) => h('th', {
              class: 'wf-table-heading',
              key: column.key,
              'data-wf-key': column.key,
            }, column.label))),
          ]),
          h('tbody', { class: 'wf-table-body' }, props.rows.map((row, index) => {
            const rowKey = props.getRowKey ? props.getRowKey(row) : (row.id ?? index)
            return h('tr', { class: 'wf-table-row', key: rowKey, 'data-wf-key': rowKey },
              props.columns.map((column) => h('td', {
                class: 'wf-table-cell',
                key: column.key,
                'data-wf-key': column.key,
              }, column.render ? column.render(row[column.key], row) : String(row[column.key] ?? ''))))
          })),
        ]),
      ])
    },
  })

  const WfTabs = defineComponent({
    name: 'WfTabs',
    inheritAttrs: false,
    props: {
      items: { type: Array, default: () => [] },
      activeId: { type: String, default: '' },
    },
    emits: ['update:activeId', 'change'],
    setup(props, { attrs, emit }) {
      return () => h('div', mergeProps(withBase(attrs, 'wf-tabs'), { role: 'tablist' }),
        props.items.map((item) => h('button', {
          class: 'wf-tab-control',
          type: 'button',
          role: 'tab',
          key: item.id,
          'aria-selected': String(item.id === props.activeId),
          onClick: () => {
            emit('update:activeId', item.id)
            emit('change', item.id)
          },
        }, item.label)))
    },
  })

  const WfSteps = defineComponent({
    name: 'WfSteps',
    inheritAttrs: false,
    props: {
      items: { type: Array, default: () => [] },
      current: { type: Number, default: 0 },
      direction: { type: String, default: 'horizontal' },
    },
    setup(props, { attrs }) {
      return () => h('ol', withBase(attrs, 'wf-steps', `wf-steps-${props.direction}`),
        props.items.map((item, index) => {
          const status = index < props.current ? 'done' : index === props.current ? 'current' : 'todo'
          return h('li', { class: `wf-steps-item wf-steps-item-${status}`, key: item.id || item.label || index }, [
            h('div', { class: 'wf-steps-indicator' }, [
              h('span', { class: 'wf-step-mark', 'aria-hidden': 'true' }, status === 'done' ? null : index + 1),
              index < props.items.length - 1 ? h('span', { class: 'wf-steps-line', 'aria-hidden': 'true' }) : null,
            ]),
            h('div', { class: 'wf-steps-content' }, [
              h('span', { class: 'wf-steps-label' }, item.label),
              item.description ? h('span', { class: 'wf-steps-desc' }, item.description) : null,
            ]),
          ])
        }))
    },
  })

  const WfEmptyState = defineComponent({
    name: 'WfEmptyState',
    inheritAttrs: false,
    props: {
      title: { type: String, default: '' },
      description: { type: String, default: '' },
    },
    setup(props, { attrs, slots }) {
      return () => h('div', withBase(attrs, 'wf-empty-state'), [
        h('span', { class: 'wf-empty-icon', 'aria-hidden': 'true' }),
        props.title ? h('strong', { class: 'wf-empty-title' }, props.title) : null,
        props.description ? h('p', { class: 'wf-empty-desc' }, props.description) : null,
        slots.action ? h('div', { class: 'wf-empty-action' }, slots.action()) : null,
      ])
    },
  })

  const ScreenOverlay = defineComponent({
    name: 'WfScreenOverlay',
    setup(_props, { slots }) {
      const anchor = ref(null)
      const target = ref(null)
      onMounted(() => {
        target.value = anchor.value && anchor.value.closest('.wf-screen-content')
      })
      return () => target.value
        ? h(Teleport, { to: target.value }, content(slots))
        : h('span', { ref: anchor, class: 'wf-overlay-anchor', 'aria-hidden': 'true' })
    },
  })

  const WfModal = defineComponent({
    name: 'WfModal',
    inheritAttrs: false,
    props: {
      open: { type: Boolean, default: false },
      title: { type: String, default: '' },
    },
    emits: ['close'],
    setup(props, { attrs, emit, slots }) {
      return () => props.open ? h(ScreenOverlay, null, {
        default: () => h('div', withBase(attrs, 'wf-overlay wf-modal-overlay'), [
          h('section', { class: 'wf-modal', role: 'dialog', 'aria-modal': 'true', 'aria-label': props.title }, [
            h('header', { class: 'wf-modal-header' }, [
              h('strong', { class: 'wf-modal-title' }, props.title),
              h(WfButton, { onClick: () => emit('close') }, { default: () => '关闭' }),
            ]),
            h('div', { class: 'wf-modal-body' }, content(slots)),
            slots.actions ? h('footer', { class: 'wf-modal-footer' }, slots.actions()) : null,
          ]),
        ]),
      }) : null
    },
  })

  const WfConfirmDialog = defineComponent({
    name: 'WfConfirmDialog',
    inheritAttrs: false,
    props: {
      open: { type: Boolean, default: false },
      title: { type: String, default: '确认操作' },
      message: { type: String, default: '' },
      confirmLabel: { type: String, default: '确认' },
      cancelLabel: { type: String, default: '取消' },
    },
    emits: ['confirm', 'cancel'],
    setup(props, { attrs, emit }) {
      return () => h(WfModal, mergeProps(attrs, {
        open: props.open,
        title: props.title,
        onClose: () => emit('cancel'),
      }), {
        default: () => h('p', { class: 'wf-confirm-message' }, props.message),
        actions: () => [
          h(WfButton, { onClick: () => emit('cancel') }, { default: () => props.cancelLabel }),
          h(WfButton, { variant: 'primary', onClick: () => emit('confirm') }, { default: () => props.confirmLabel }),
        ],
      })
    },
  })

  function overlayStatus(name, baseClass, defaultLabel) {
    return defineComponent({
      name,
      inheritAttrs: false,
      props: {
        open: { type: Boolean, default: false },
        label: { type: String, default: defaultLabel },
      },
      setup(props, { attrs, slots }) {
        return () => props.open ? h(ScreenOverlay, null, {
          default: () => h('div', mergeProps(withBase(attrs, `wf-overlay ${baseClass}`), { role: 'status' }),
            slots.default ? slots.default() : props.label),
        }) : null
      },
    })
  }

  const WfToast = overlayStatus('WfToast', 'wf-toast', '')

  const WfLoadingOverlay = defineComponent({
    name: 'WfLoadingOverlay',
    inheritAttrs: false,
    props: {
      open: { type: Boolean, default: false },
      label: { type: String, default: '加载中' },
    },
    setup(props, { attrs }) {
      return () => props.open ? h(ScreenOverlay, null, {
        default: () => h('div', mergeProps(withBase(attrs, 'wf-overlay wf-loading'), { role: 'status' }), [
          h('span', { class: 'wf-loading-shape', 'aria-hidden': 'true' }),
          h('span', { class: 'wf-loading-label' }, props.label),
        ]),
      }) : null
    },
  })

  const WfWireMap = defineComponent({
    name: 'WfWireMap',
    inheritAttrs: false,
    setup(_props, { attrs, slots }) {
      return () => h('div', mergeProps(withBase(attrs, 'wf-map'), { style: { position: 'relative' } }), [
        h('span', { class: 'wf-map-line wf-map-line-a', 'aria-hidden': 'true' }),
        h('span', { class: 'wf-map-line wf-map-line-b', 'aria-hidden': 'true' }),
        ...content(slots),
      ])
    },
  })

  const WfMapMarker = defineComponent({
    name: 'WfMapMarker',
    inheritAttrs: false,
    props: {
      x: { type: Number, required: true },
      y: { type: Number, required: true },
      label: { type: String, default: '' },
      to: { type: String, default: '' },
    },
    setup(props, { attrs }) {
      return () => h('button', mergeProps(withFlow(attrs, props.to, 'wf-map-marker'), {
        type: 'button',
        'aria-label': props.label,
        style: { left: `${props.x}%`, top: `${props.y}%` },
      }), [h('span', { class: 'wf-map-marker-shape', 'aria-hidden': 'true' })])
    },
  })

  const WfMapOverlay = defineComponent({
    name: 'WfMapOverlay',
    inheritAttrs: false,
    props: { position: { type: String, default: 'bottom' } },
    setup(props, { attrs, slots }) {
      return () => h('div', withBase(attrs, 'wf-map-overlay', `wf-map-overlay-${props.position}`), content(slots))
    },
  })

  const components = Object.freeze({
    WfBox,
    WfRow,
    WfColumn,
    WfGrid,
    WfHeading,
    WfText,
    WfCard,
    WfBadge,
    WfAvatar,
    WfImagePlaceholder,
    WfButton,
    WfTextInput,
    WfTextArea,
    WfSelect,
    WfCheckbox,
    WfRadio,
    WfToggle,
    WfFormField,
    WfPageHeader,
    WfSideNav,
    WfTabBar,
    WfBreadcrumbs,
    WfMobileShell,
    WfCell,
    WfDataTable,
    WfTabs,
    WfSteps,
    WfEmptyState,
    WfModal,
    WfConfirmDialog,
    WfToast,
    WfLoadingOverlay,
    WfWireMap,
    WfMapMarker,
    WfMapOverlay,
  })

  Wireframe.setUiInstaller((app) => {
    Object.entries(components).forEach(([name, component]) => app.component(name, component))
  })
})(window)
