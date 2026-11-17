#! /bin/bash

# Param1：传入源码目录
BASE_DIR=$1
cd $BASE_DIR/kwbase

echo "=============Start to run golang unit test============="
# 运行golang单元测试
make -f Makefile_ent test LIBPROTOBUF=${GOPATH}/native/kwdbts2/third_party/lib/libprotobuf.a PROTOBUF_INC=${GOPATH}/native/kwdbts2/third_party/include PROTOBUF_C=${GOPATH}/native/kwdbts2/third_party/bin/protoc TESTTIMEOUT=45m KWDB_LIB_DIR=${BASE_DIR}/build/lib
