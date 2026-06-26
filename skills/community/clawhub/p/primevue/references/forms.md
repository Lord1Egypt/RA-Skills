# PrimeVue Forms

## Installation

```bash
npm install @primevue/forms
```

## Basic Usage

```vue
<template>
    <Form
        v-slot="$form"
        :initialValues="{ username: '', email: '' }"
        :resolver="resolver"
        @submit="onSubmit"
        class="flex flex-col gap-4 w-56"
    >
        <div class="flex flex-col gap-1">
            <InputText name="username" type="text" placeholder="Username" fluid />
            <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
                {{ $form.username.error.message }}
            </Message>
        </div>

        <div class="flex flex-col gap-1">
            <InputText name="email" type="email" placeholder="Email" fluid />
            <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">
                {{ $form.email.error.message }}
            </Message>
        </div>

        <Button type="submit" severity="secondary" label="Submit" />
    </Form>
</template>

<script setup>
import { Form } from '@primevue/forms';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Message from 'primevue/message';

const resolver = (values) => {
    const errors = {};

    if (!values.username) {
        errors.username = [{ message: 'Username is required.' }];
    }

    if (!values.email) {
        errors.email = [{ message: 'Email is required.' }];
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
        errors.email = [{ message: 'Invalid email format.' }];
    }

    return { values: {}, errors };
};

const onSubmit = ({ values, errors }) => {
    if (errors) return;  // validation failed
    console.log(values);  // { username: '...', email: '...' }
};
</script>
```

## With Zod

```vue
<script setup>
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
    username: z.string().min(1, 'Username is required'),
    email: z.string().email('Invalid email')
});

const resolver = zodResolver(schema);
</script>
```

## With Yup

```vue
<script setup>
import { yupResolver } from '@primevue/forms/resolvers/yup';
import * as yup from 'yup';

const schema = yup.object({
    username: yup.string().required('Username is required'),
    email: yup.string().email('Invalid email').required('Email is required')
});

const resolver = yupResolver(schema);
</script>
```

## Other Resolvers

```vue
// Valibot
import { valibotResolver } from '@primevue/forms/resolvers/valibot';

// Joi
import { joiResolver } from '@primevue/forms/resolvers/joi';

// Superstruct
import { superstructResolver } from '@primevue/forms/resolvers/superstruct';
```

## Form State

The `v-slot="$form"` provides access to form state:

| Property | Description |
|----------|-------------|
| `$form.username` | Field state for "username" |
| `$form.username.value` | Current value |
| `$form.username.error` | Error object `{ message }` |
| `$form.username.invalid` | Boolean — has errors |
| `$form.username.dirty` | Boolean — value changed |

## Field State Object

```ts
interface FieldState {
    value: any;
    error: { message: string } | null;
    invalid: boolean;
    dirty: boolean;
    touched: boolean;
    required: boolean;
}
```

## Dynamic Forms

### Declarative

```vue
<DynamicForm @submit="onSubmit">
    <DynamicFormField groupId="g1" name="firstName">
        <DynamicFormLabel>First Name</DynamicFormLabel>
        <DynamicFormControl as="InputText" defaultValue="Jane" />
        <DynamicFormMessage />
    </DynamicFormField>

    <DynamicFormField groupId="g2" name="lastName">
        <DynamicFormLabel>Last Name</DynamicFormLabel>
        <DynamicFormControl as="InputText" />
        <DynamicFormMessage />
    </DynamicFormField>

    <DynamicFormSubmit />
</DynamicForm>
```

### Programmatic

```vue
<DynamicForm :fields :resolver @submit="onSubmit" />
```

## Nested Values

```vue
<Form :initialValues="{ user: { name: '', email: '' } }">
    <InputText name="user.name" />
    <InputText name="user.email" />
</Form>
```

## Array Values

```vue
<Form :initialValues="{ items: ['', '', ''] }">
    <InputText v-for="(item, index) in items" :key="index" :name="`items.${index}`" />
</Form>
```

## Form Actions

```vue
const reset = () => formRef.value.reset();
const submit = () => formRef.value.submit();
```

## Validation Triggers

By default, validation runs on submit. To validate on blur/touch:

```vue
<InputText
    name="email"
    @blur="() => $form.email?.validate()"
/>
```

## Password with Strength

```vue
<DynamicFormField name="password">
    <DynamicFormLabel>Password</DynamicFormLabel>
    <DynamicFormControl as="Password" toggleMask fluid :schema="passwordSchema" />
    <DynamicFormMessage errorType="minimum" />
    <DynamicFormMessage errorType="maximum" />
    <DynamicFormMessage errorType="uppercase" severity="warn" />
    <DynamicFormMessage errorType="lowercase" severity="warn" />
    <DynamicFormMessage errorType="number" severity="secondary" />
</DynamicFormField>
```

## Message Component

```vue
<Message
    severity="error"      // error, warn, info, success, secondary
    size="small"           // small, normal
    variant="simple"       // simple, inline, toast (uses Toast service)
>
    Error message text
</Message>
```

## Locale / i18n

Form messages can be localized via the PrimeVue locale configuration:

```vue
app.use(PrimeVue, {
    locale: {
        startsWith: 'Starts with',
        contains: 'Contains',
        notContains: 'Not contains',
        endsWith: 'Ends with',
        equals: 'Equals',
        notEquals: 'Not equals',
        noFilter: 'No Filter',
        lt: 'Less than',
        lte: 'Less than or equal to',
        gt: 'Greater than',
        gte: 'Greater than or equal to',
        // ... more
    }
});
```

## Common Patterns

### Fluid Layout (full width)

```vue
<InputText name="username" fluid />
<!-- instead of -->
<div class="w-full">
    <InputText name="username" class="w-full" />
</div>
```

### Conditional Field

```vue
<template v-if="$form.type?.value === 'advanced'">
    <InputNumber name="price" />
</template>
```

### Submit Button State

```vue
<Button
    type="submit"
    label="Submit"
    :loading="$form.pending"
/>
```
