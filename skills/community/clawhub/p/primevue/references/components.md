# PrimeVue Components Quick Reference

## Install All Components

```bash
npm install primevue
```

Or import individually for tree-shaking:
```bash
npm install primevue button inputtext textarea select checkbox radiobutton
```

## Auto Import (Recommended)

```bash
npm install primevue @primevue/auto-import
```

```vue
// vite.config.js
import PrimeVueAutoImport from '@primevue/auto-import';
export default {
    plugins: [PrimeVueAutoImport()]
};
```

## Button

```vue
<Button label="Save" icon="pi pi-check" />
<Button label="Delete" severity="danger" outlined />
<Button label="Loading" :loading="true" />
<Button label="Link" link />
<Button label="Badge" badge="3" />

<!-- Severity: primary, secondary, success, info, warn, danger, help -->
<!-- Variants: text, outlined, filled -->
```

## InputText

```vue
<InputText v-model="value" placeholder="Enter text" />
<InputText :modelValue="value" @update:modelValue="v => value = v" />
```

## Textarea

```vue
<Textarea v-model="value" rows="5" autoResize />
```

## InputNumber

```vue
<InputNumber v-model="value" />
<InputNumber v-model="price" mode="currency" currency="USD" locale="en-US" />
<InputNumber v-model="percent" suffix="%" />
```

## Select (Dropdown)

```vue
<Select v-model="selected" :options="options" optionLabel="name" optionValue="code" placeholder="Select" />
```

## MultiSelect

```vue
<MultiSelect v-model="selected" :options="options" optionLabel="name" optionValue="code" placeholder="Select" :maxSelectedLabels="3" />
```

## Checkbox

```vue
<Checkbox v-model="checked" :binary="true" />
<Checkbox v-model="selected" :value="['A', 'B']" />

<Checkbox name="city" value="NYC" v-model="selected" label="New York" />
```

## RadioButton

```vue
<RadioButton name="city" value="NYC" v-model="selected" />
<RadioButton name="city" value="SFO" v-model="selected" />
```

## ToggleSwitch

```vue
<ToggleSwitch v-model="enabled" />
```

## ToggleButton

```vue
<ToggleButton v-model="state" onLabel="On" offLabel="Off" />
```

## SelectButton

```vue
<SelectButton v-model="size" :options="['S', 'M', 'L']" />
```

## DatePicker

```vue
<DatePicker v-model="date" />
<DatePicker v-model="range" selectionMode="range" />
<DatePicker v-model="dates" selectionMode="multiple" />
<DatePicker v-model="month" view="month" dateFormat="mm" />
```

## Password

```vue
<Password v-model="password" :feedback="true" toggleMask />
```

## InputMask

```vue
<InputMask mask="99/99/9999" v-model="value" placeholder="99/99/9999" />
<InputMask mask="(999) 999-9999" v-model="phone" />
```

## Knob

```vue
<Knob v-model="value" :step="10" />
```

## Slider

```vue
<Slider v-model="value" />
<Slider v-model="range" :range="true" />
```

## Rating

```vue
<Rating v-model="value" />
<Rating v-model="value" :cancel="false" />
```

## ColorPicker

```vue
<ColorPicker v-model="color" />
```

## FileUpload

```vue
<FileUpload mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000" />
<FileUpload mode="advanced" @select="onSelect" :multiple="true" />
```

## Dialog (Modal)

```vue
<Dialog v-model:visible="show" header="Title" :style="{ width: '50vw' }" :modal="true">
    Content here
    <template #footer>
        <Button label="Cancel" text @click="show = false" />
        <Button label="Save" @click="show = false" />
    </template>
</Dialog>

<!-- v-model:visible to open/close -->
```

## Drawer (Side Panel)

```vue
<Drawer v-model:visible="show" position="right" :style="{ width: '300px' }">
    Sidebar content
</Drawer>

<!-- position: left, right, top, bottom -->
```

## Toast

```vue
<!-- In App.vue -->
<Toast />

<!-- In your component -->
<script setup>
import { useToast } from 'primevue/usetoast';
const toast = useToast();

toast.add({ severity: 'success', summary: 'Saved', detail: 'Your changes were saved', life: 3000 });
toast.add({ severity: 'error', summary: 'Error', detail: 'Something went wrong', sticky: true });
toast.add({ severity: 'warn', summary: 'Warning', detail: 'Check your input' });
toast.add({ severity: 'info', summary: 'Info', detail: 'New version available' });
</script>
```

## ConfirmDialog

```vue
<script setup>
import { useConfirm } from 'primevue/useconfirm';
const confirm = useConfirm();

confirm.require({
    message: 'Are you sure you want to proceed?',
    header: 'Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => { /* handle */ },
    reject: () => { /* handle */ }
});
</script>

<ConfirmDialog />
```

## Panel

```vue
<Panel header="Header">
    Content
    <template #toggler="{ collapsed }">
        {{ collapsed ? 'Expand' : 'Collapse' }}
    </template>
</Panel>

<Panel :toggleable="true" :collapsed="true">
    Collapsible content
</Panel>
```

## Card

```vue
<Card>
    <template #title> Card Title </template>
    <template #subtitle> Subtitle </template>
    <template #content> Content </template>
    <template #footer> Footer </template>
</Card>
```

## Accordion

```vue
<Accordion>
    <AccordionPanel value="0">
        <AccordionHeader>Panel 1</AccordionHeader>
        <AccordionContent>Content 1</AccordionContent>
    </AccordionPanel>
    <AccordionPanel value="1">
        <AccordionHeader>Panel 2</AccordionHeader>
        <AccordionContent>Content 2</AccordionContent>
    </AccordionPanel>
</Accordion>
```

## Tabs

```vue
<Tabs value="0">
    <TabList>
        <Tab value="0">Tab 1</Tab>
        <Tab value="1">Tab 2</Tab>
    </TabList>
    <TabPanels>
        <TabPanel value="0">Content 1</TabPanel>
        <TabPanel value="1">Content 2</TabPanel>
    </TabPanels>
</Tabs>
```

## Toolbar

```vue
<Toolbar>
    <template #start>
        <Button label="New" icon="pi pi-plus" />
        <Button label="Open" icon="pi pi-folder-open" outlined />
    </template>
    <template #end>
        <Button label="Save" icon="pi pi-save" />
    </template>
</Toolbar>
```

## Menu

```vue
<Menu :model="menuItems" />
<!-- menuItems: [{ label: 'File', items: [...] }, ...] -->

<Button label="Menu" @click="toggle" />
<Menu ref="menu">
    <template #start>Header</template>
    <template #end>Footer</template>
</Menu>
```

## Breadcrumb

```vue
<Breadcrumb :home="home" :model="items" />
<!-- items: [{ label: 'Category' }, { label: 'Subcategory' }] -->
```

## DataTable

```vue
<DataTable :value="products" paginator :rows="10" :loading="loading">
    <Column field="name" header="Name" sortable />
    <Column field="price" header="Price" sortable>
        <template #body="{ data }">${{ data.price }}</template>
    </Column>
    <Column header="Actions">
        <template #body="{ data }">
            <Button icon="pi pi-pencil" @click="edit(data)" />
            <Button icon="pi pi-trash" severity="danger" @click="remove(data)" />
        </template>
    </Column>
</DataTable>
```

## DataView

```vue
<DataView :value="items" layout="grid">
    <template #list="{ items }">
        <div v-for="item in items">{{ item.name }}</div>
    </template>
    <template #grid="{ items }">
        <div v-for="item in items" class="col-12 md:col-4">{{ item.name }}</div>
    </template>
</DataView>
```

## Tree

```vue
<Tree v-model:selectionKeys="selected" :value="treeData" selectionMode="checkbox" />
```

## TreeSelect

```vue
<TreeSelect v-model="selectedNode" :options="treeData" placeholder="Select" />
```

## TreeTable

```vue
<TreeTable :value="treeData">
    <Column field="name" header="Name" />
    <Column field="size" header="Size" />
</TreeTable>
```

## Paginator

```vue
<Paginator
    :rows="10"
    :totalRecords="100"
    :first="first"
    @page="onPage($event)"
    :rowsPerPageOptions="[10, 20, 50]"
/>
```

## Tag

```vue
<Tag value="New" severity="success" />
<Tag value="Outlined" variant="outlined" />
```

## Badge

```vue
<Badge value="3" />
<Button label="Notifications" badge="99" />
```

## Chip

```vue
<Chip label="Apple" icon="pi pi-apple" removable @remove="remove" />
```

## Avatar

```vue
<Avatar label="P" shape="circle" />
<Avatar image="/photo.jpg" size="large" />
<AvatarGroup>
    <Avatar image="/p1.jpg" />
    <Avatar image="/p2.jpg" />
</AvatarGroup>
```

## Skeleton

```vue
<Skeleton width="10rem" height="2rem" />
<Skeleton shape="circle" size="3rem" />
```

## ProgressBar

```vue
<ProgressBar :value="progress" />
<ProgressBar mode="indeterminate" />
```

## ProgressSpinner

```vue
<ProgressSpinner />
```

## Tooltip

```vue
<Button label="Help" tooltip="Click for help" />
<Button label="Details">
    <template #tooltip>
        More information here
    </template>
</Button>

<!-- Directive -->
<Button v-tooltip.bottom="'Tooltip text'" label="Help" />
```

## Popover

```vue
<Button label="Toggle" @click="toggle" />
<Popover ref="op">
    <div class="p-2">Popover content</div>
</Popover>
```

## InlineMessage

```vue
<InlineMessage severity="warn">Warning message</InlineMessage>
```

## Message

```vue
<Message severity="success" :closable="false">Saved successfully</Message>
```

## Divider

```vue
<Divider />
<Divider align="left" type="dashed">Or</Divider>
```

## Stepper

```vue
<Stepper value="1">
    <StepList>
        <Step value="0">Step 1</Step>
        <Step value="1">Step 2</Step>
        <Step value="2">Step 3</Step>
    </StepList>
    <StepPanels>
        <StepPanel value="0">Content 1</StepPanel>
        <StepPanel value="1">Content 2</StepPanel>
        <StepPanel value="2">Content 3</StepPanel>
    </StepPanels>
</Stepper>
```

## Carousel

```vue
<Carousel :value="items" :numVisible="3" :numScroll="1">
    <template #item="{ data }">{{ data.name }}</template>
</Carousel>
```

## Galleria

```vue
<Galleria :value="images" :numVisible="5">
    <template #item="{ item }">
        <img :src="item.src" />
    </template>
    <template #thumbnail="{ item }">
        <img :src="item.src" />
    </template>
</Galleria>
```

## Image

```vue
<Image src="/photo.jpg" alt="Description" preview />
```

## OrganizationChart

```vue
<OrganizationChart :value="data">
    <template #default="{ node }">{{ node.label }}</template>
</OrganizationChart>
```

## Terminal

```vue
<Terminal welcomeMessage="PrimeVue Terminal" @command="handleCommand" />
```

## BlockUI

```vue
<BlockUI :blocked="loading">
    <DataTable :value="products" />
</BlockUI>
```

## ContextMenu

```vue
<ContextMenu ref="cm" :model="menuItems" />

<div @contextmenu="cm.toggle($event)">Right click me</div>
```

## OverlayPanel

```vue
<Button label="Toggle" @click="op.toggle($event)" />
<OverlayPanel ref="op">
    <p>Content</p>
</OverlayPanel>
```

## Splitter

```vue
<Splitter>
    <SplitterPanel :size="30">Left</SplitterPanel>
    <SplitterPanel :size="70">Right</SplitterPanel>
</Splitter>
```

## VirtualScroller

```vue
<VirtualScroller :items="largeList" :itemSize="50">
    <template #item="{ item }">{{ item }}</template>
</VirtualScroller>
```

## OrderList

```vue
<OrderList v-model="list" />
```

## PickList

```vue
<PickList v-model="list" sourceHeader="Available" targetHeader="Selected" />
```

## Timeline

```vue
<Timeline :value="events" align="left">
    <template #marker="{ item }">{{ item.marker }}</template>
    <template #content="{ item }">{{ item.text }}</template>
</Timeline>
```

## Terminal

```vue
<Terminal welcomeMessage="Welcome to PrimeVue Terminal" @command="handleCommand" />
```

## SpeedDial

```vue
<SpeedDial :model="items" direction="up" />
```

## Dock

```vue
<Dock :model="items" position="left">
    <template #item="{ item }">
        <img :src="item.icon" />
    </template>
</Dock>
```

## DeferredContent

```vue
<DeferredContent @load="onLoad">
    <HeavyComponent />
</DeferredContent>
```

## AnimateOnScroll

```vue
<div v-animateonscroll="'animate-fade-in'">Animates on scroll</div>
```

## FocusTrap

```vue
<Dialog v-model:visible="show" :modal="true" :pt="{ mask: { focusTrap: true } }">
    Focus trapped inside
</Dialog>
```

## StyleClass

```vue
<div v-styleclass="{ selector: '@next', toggleClass: 'hidden' }">
    Toggle next element
</div>
```

## InputOtp

```vue
<InputOtp v-model="value" :length="6" />
```
