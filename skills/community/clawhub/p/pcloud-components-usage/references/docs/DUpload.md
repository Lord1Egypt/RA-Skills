---
title: DUpload
description: 基于 antd 4.24.10 Upload 的二次封装组件
tocDepth: 2
nav:
  title: 组件
  path: /components
group:
  title: 业务组件
---

# DUpload 上传组件

DUpload 是基于 Ant Design Upload 组件的增强封装，专门优化了图片上传体验和表单集成能力，提供自动缩略图生成、便捷的预览和下载功能，适用于各种文件上传场景。

## 组件特性

- 🖼️ 图片上传优化，自动为图片格式生成 base64 缩略图预览
- ⚙️ 异步操作支持，onPreview、onDownload 均支持 Promise 异步处理
- 🎨 表单集成优化，解决 Form 禁用状态下图标被意外禁用的问题
- 🧩 灵活的文件管理，支持受控和非受控两种模式
- 📁 预览功能增强，支持非图片类文件的预览按钮显示

## 基础用法

<code src="./demos/basicDemo.tsx" title="基础用法" description="最基本的上传用法，与antd中的Upload用法一致，上传图像时默认对本地预览图像进行适当压缩"></code>

## 表单中使用

<code src="./demos/uploadInFormDemo.tsx" title="表单中使用" description="在form表单中作为表单项元素使用"></code>

## 生成缩略图

<code src="./demos/thumbDemo.tsx" title="生成缩略图" description="当上传文件为图像时，自动生成缩略图，图像文件过大时，还可以对缩略图进行压缩"></code>

## 自定义上传及删除

<code src="./demos/listDemo.tsx" title="自定义上传及删除" description="通过fileList搭配customRequest、onRemove可以实现完全受控的上传列表"></code>

## 图像下载及预览

<code src="./demos/previewDemo.tsx" title="图像下载及预览" description="通过enablePreview强制对非图像文件进行预览,使用优化过的onPreview、onDownload控制下载及预览的细节"></code>

## API

### DUploadProps

DUpload 继承了 Ant Design Upload 的所有属性。

| 参数          | 说明                                                                                            | 类型                                                                                                                      | 默认值 |
| ------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------ |
| value         | 初始文件列表(相当于 defaultFileList,但优先级高于 defaultFileList)                               | `DUploadFile` \| `DUploadFile[]`                                                                                          | -      |
| fileList      | 文件列表(在 Form 组件中表现为受控列表，在一般情况下相当于初始文件列表，其优先级高于 value 属性) | `DUploadFile` \| `DUploadFile[]`                                                                                          | -      |
| onChange      | 文件列表变化时的回调函数                                                                        | `(list: DUploadFile[], info: UploadChangeParam<DUploadFile>) => void`                                                     | -      |
| customRequest | 文件上传时的回调函数，支持 Promise                                                              | `(file: DUploadFile, list: DUploadFile[], requestOption: any) => DUploadFile[] \| Promise<DUploadFile[] \| void> \| void` | -      |
| onRemove      | 点击删除按钮时的回调，支持 Promise                                                              | `(file: DUploadFile, list: DUploadFile[]) => DUploadFile[] \| Promise<DUploadFile[] \| void> \| void`                     | -      |
| onDownload    | 点击下载按钮时的回调，支持 Promise                                                              | `(file: DUploadFile) => DUploadFile \| Blob \| Promise<DUploadFile \| Blob> \| void`                                      | -      |
| onPreview     | 点击预览按钮时的回调，支持 Promise                                                              | `(file: DUploadFile) => DUploadFile \| Blob \| Promise<DUploadFile \| Blob> \| void`                                      | -      |
| uploadButton  | 上传按钮，等同于 children 但优先于 children                                                     | `ReactNode`                                                                                                               | -      |
| thumbOption   | 上传文件时的缩略图选项,null 表示不生成缩略图                                                    | `ThumbOptionProps` \| `null`                                                                                              | -      |
| itemClassName | 列表项样式类名                                                                                  | `string`                                                                                                                  | -      |
| enablePreview | 是否启用预览功能                                                                                | `boolean` \| `((file: DUploadFile) => boolean)`                                                                           | false  |

其他属性同 antd Upload 组件，详见：https://4x-ant-design.antgroup.com/components/upload-cn/#API

### DUploadFile

扩展自 Ant Design 的 UploadFile。

| 参数   | 说明                                               | 类型                                                       | 默认值 |
| ------ | -------------------------------------------------- | ---------------------------------------------------------- | ------ |
| id     | 文件 id                                            | `string` \| `number`                                       | -      |
| uid    | 文件 uid,系统自动生成                              | `string` \| `number`                                       | -      |
| source | 文件来源 upload:文件对话框,remote:已上传的文件对象 | `upload` \| `remote`                                       | -      |
| status | 文件状态                                           | `error` \| `success` \| `done` \| `uploading` \| `removed` | -      |

继承自 UploadFile，附带额外属性用于渲染，详见：https://4x-ant-design.antgroup.com/components/upload-cn/#UploadFile

### ThumbOptionProps

缩略图选项配置。

| 参数        | 说明                                                                   | 类型                                                               | 默认值                                                      |
| ----------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------- |
| filter      | 对目标文件进行过滤，默认只对图片格式生成缩略图                         | `((file: DUploadFile) => boolean)` \| `Array<string>`              | `['image/gif', 'image/jpeg', 'image/png', 'image/svg+xml']` |
| size        | 文件大小,当上传文件大于指定值时会对缩略图进行压缩,单位为字节，默认 2MB | `number`                                                           | `2097152`                                                   |
| compress    | 缩略图压缩参数,默认为 {width:300,height:200,quality:0.7}               | `CompressProps` \| `null`                                          | `{ width: 300, height: 200, quality: 0.7 }`                 |
| onError     | 缩略图生成失败时的回调函数                                             | `(err: Error) => void`                                             | -                                                           |
| getThumbUrl | 自定义生成 base64 缩略图的方法                                         | `(file: DUploadFile, option: ThumbOptionProps) => Promise<string>` | -                                                           |

### DUpload.imageToBase64 方法

imageToBase64 方法用于将图像格式的文件转换为 base64 格式,可以使用 compress 参数对 base64 进行适当的压缩以减小体积

##### 声明格式

```jsx {0} | pure
function imageToBase64(blob: Blob, compress?: CompressProps | null): Promise<string>
```

##### 用法示例

```jsx {0} | pure
import { DUpload } from '@pointcloud/pcloud-components';
const { imageToBase64 } = DUpload;

imageToBase64(file, { width: 300, height: 200, quality: 0.7 }).then((url) => {
  console.log(url);
});
```
