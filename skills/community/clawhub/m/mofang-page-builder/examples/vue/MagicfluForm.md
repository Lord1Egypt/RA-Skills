# Vue Create Form Example

Copy the component below into a `.vue` file in the user's project when Vue is the chosen stack. The skill package keeps it as Markdown because some skill uploaders reject `.vue` files as "non-text" even though the content is plain text.

```vue
<template>
  <form class="magicflu-form" @submit.prevent="onSubmit">
    <label>
      Name
      <input v-model="form.mingcheng" type="text" />
    </label>
    <label>
      Amount
      <input v-model="form.jine" type="number" step="0.01" />
    </label>
    <button type="submit">Submit</button>
    <p v-if="message">{{ message }}</p>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';

const CONFIG = {
  apiBase: '', // local debug: 'http://127.0.0.1:3847'; same-origin production: ''
  spaceId: 'YOUR_SPACE_ID',
  formId: 'YOUR_FORM_ID',
};

const form = reactive({
  mingcheng: '',
  jine: '',
});

const message = ref('');

function apiUrl(path: string): string {
  const origin = CONFIG.apiBase ? CONFIG.apiBase.replace(/\/$/, '') : '';
  return `${origin}${path}`;
}

function collectData(): Record<string, string | number> {
  const data: Record<string, string | number> = {};
  if (form.mingcheng.trim()) data.mingcheng = form.mingcheng.trim();
  if (form.jine.trim()) {
    const amount = Number(form.jine);
    if (Number.isFinite(amount)) data.jine = amount;
  }
  return data;
}

async function onSubmit() {
  const data = collectData();
  if (!Object.keys(data).length) {
    message.value = 'Please fill at least one field.';
    return;
  }

  const path = `/magicflu/service/s/jsonv2/${CONFIG.spaceId}/forms/${CONFIG.formId}/records`;
  const res = await fetch(apiUrl(path), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json().catch(() => ({}));

  if (!res.ok || (json.errcode && json.errcode !== '0')) {
    throw new Error(json.errmsg || 'Create record failed.');
  }
  message.value = `Created record: ${json.id || ''}`;
  form.mingcheng = '';
  form.jine = '';
}
</script>

<style scoped>
.magicflu-form {
  display: grid;
  gap: 12px;
  max-width: 480px;
}

label {
  display: grid;
  gap: 4px;
}
</style>
```
