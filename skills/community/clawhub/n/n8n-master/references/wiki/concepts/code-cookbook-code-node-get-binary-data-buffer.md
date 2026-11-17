# Get the binary data buffer

## 何时读取

当用户的问题涉及 n8n 文档 `code/cookbook/code-node/get-binary-data-buffer.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- The binary data buffer contains all the binary file data processed by a workflow. You need to access it if you want to perform operations on the binary data, such as: ```js /* * itemIndex: number. The index of the item in the input data. * binaryPropertyName: string. The name of the binary property. * The default in the Read/Write File From Disk node is 'data'. */ let binaryDataBufferItem = await this.helpers.getBinaryDataBuffer(itemIndex, binaryPropertyName); ```

## 快速定位

- 源文档没有稳定二级标题；需要完整细节时回读 source。

