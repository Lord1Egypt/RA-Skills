# mouse-yolo-factory

這是一個專為老鼠 (Mouse) 產品瑕疵檢測開發的 YOLO 整合技能。支援瑕疵影像生成、自動化模型推論標記，以及資料集的合併與版本管理。

## Metadata
- id: mouse-yolo-factory
- kind: package
- label: Mouse YOLO Factory
- owner: Alex Ho

## Usage

### 1. 瑕疵生成 (Scratch Generation)
在原始影像上模擬生成劃傷 (Scratch) 瑕疵。
`python D:/aiagent/aiagent_for_Mouse_Python_code/Mouse_produce_scratch.py --input <input_dir> --output <output_dir>`

### 2. 模型推論與自動標記 (Auto-Labeling)
使用現有模型進行推論，並將結果儲存為 JSON/YOLO 格式。
`python D:/aiagent/aiagent_for_Mouse_Python_code/drawbox_and_dataset_savejson_with_model.py --model <model_path> --img_size <size> --conf <threshold> --source <img_path>`

### 3. 資料集合併與融合 (Dataset Merge)
將新標記好的資料併入全域資料庫。
`python D:/aiagent/aiagent_for_Mouse_Python_code/datatool.py --new_data <new_path> --yolo_db <db_root> --desc <description>`

## Use when
- 使用者想要透過演算法在老鼠圖片上「產生」、「模擬」或「製作」劃傷瑕疵時。
- 使用者需要使用現有的 YOLO 模型對新圖片進行「推論」、「預標記」或「自動框選」時。
- 使用者提到「合併資料」、「融合數據集」、「建立新版本」或「將新資料歸檔」時。

## Don't use when
- 進行硬體自動化測試（如 ADB 或 PLC 控制）時。
- 僅需進行單純的文件移動或重新命名，不涉及資料集邏輯時。