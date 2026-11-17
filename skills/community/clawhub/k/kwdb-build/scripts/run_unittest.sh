#! /bin/bash

# Param：传入源码目录
BASE_DIR=$1
cd $BASE_DIR/test

echo "=============Start to run unit test============="
# 运行单元测试
for case_dir in $(find $(pwd) -maxdepth 1 -type d -name "*.dir"); do
    case_name=$(basename ${case_dir} | grep -Po ".*(?=\.dir)")
    echo "****************单项测试开始: ${case_name}****************"
    cd ${case_dir}
    # 运行单项测试脚本
    if [ -f $case_name ];then
        chmod +x $case_name
        ./$case_name
    else
        echo "未找到单项测试脚本: $case_name"
    fi
    echo "****************单项测试结束: ${case_name}****************"
    cd ..
done
