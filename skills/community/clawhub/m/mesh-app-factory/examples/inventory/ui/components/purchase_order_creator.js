// 采购订单创建/详情组件
import productSelector from './product_selector.js';
import supplierSelector from './supplier_selector.js';

function completeOrder(orderId,onSuccess,onError){
  request({method:"PUT",url:"/api/purchase/completeOrder",data:{id:orderId}},"inventory").then(resp=>{
    if(resp.code!=RetCode.OK){
      onError(resp.code,resp.info);
      return;
    }
    onSuccess(orderId)
  })
}

function cancelOrder(orderId,onSuccess,onError) {
  request({method:"DELETE",url:"/api/purchase/cancelOrder?id="+orderId},"inventory").then(resp=>{
    if(resp.code!=RetCode.OK){
      onError(resp.code,resp.info);
      return;
    }
    onSuccess(orderId)
  })
}

export {completeOrder, cancelOrder};

export default {
inject:['tags','service'],
components:{productSelector, supplierSelector},
data(){return{
  showDialog:false,
  status:0, //2:add,0:edit,1:view
  orderItems:[],
  newItem:{product:{id:null, name:'',price:0},quantity:1,unitPrice:0,subTotal:0},
  curOrder:{id:null, supplier:{id:0, name:'Unknown'},totalAmount:0,remark:''}
}},

emits:['orderCompleted','orderCanceled','hide'],

methods:{
  // 通过扫码快速添加商品
  scanAndAdd(){
    Platform.scanCode().then(result=>{
      if(!result || !result.text){
        this.$refs.errMsg.show(this.tags.scanFailed||'扫码失败');
        return;
      }
      var barcode=result.text;
      request({method:"GET",url:"/api/product/search?keyword="+encodeURIComponent(barcode)+"&limit=1"},this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK || !resp.data.list || resp.data.list.length===0){
          this.$refs.errMsg.show(this.tags.productNotFound);
          return;
        }
        var product=resp.data.list[0];
        // 检查是否已存在
        var existing=this.orderItems.find(i=>i.productId===product.id);
        if(existing){
          existing.quantity++;
          existing.subTotal=(existing.quantity*existing.unitPrice).toFixed(2);
        }else{
          this.orderItems.push({
            productId:product.id,
            productName:product.name,
            quantity:1,
            unitPrice:product.price,
            subTotal:product.price.toFixed(2)
          });
        }
        this.calcTotal();
      });
    }).catch(err=>{
      this.$refs.errMsg.show(this.tags.scanFailed||'扫码失败: '+err);
    });
  },

  addItemToList(){
    if(!this.newItem.product.id){this.$refs.errMsg.show(this.tags.pleaseSelectProduct);return;}
    if(this.newItem.quantity<=0){this.$refs.errMsg.show(this.tags.pleaseInputQuantity);return;}

    if(this.curOrder.id){
      this.doAddItem();
      return;
    }
    this.calcTotal();
    var orderData={
      supplierId:this.curOrder.supplier.id,
      remark:this.curOrder.remark
    };
    request({method:"POST",url:"/api/purchase/createOrder",data:orderData},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info);
        return;
      }
      this.curOrder.id=resp.data.id;
      this.doAddItem();
    });
  },

  doAddItem(){
    var itemData={
      orderId:this.curOrder.id,
      productId:this.newItem.product.id,
      productName:this.newItem.product.name,
      quantity:this.newItem.quantity,
      unitPrice:this.newItem.product.price
    };
    request({method:"POST",url:"/api/purchase/addItem",data:itemData},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info)
        return;
      }

      var item={...itemData,subTotal:this.newItem.subTotal};
      this.orderItems.push(item);
      this.calcTotal();
      this.newItem={product:{id:null, name:'',price:0},quantity:1,unitPrice:0,subTotal:0}
    });
  },

  doRemoveItem(idx){
    var itemData=this.orderItems[idx];
    var url="/api/purchase/removeItem?orderId=" + itemData.orderId + "&productId=" + itemData.productId;
    request({method:"DELETE",url:url}, this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
          this.$refs.errMsg.showErr(resp.code,resp.info)
          return;
      }
      this.orderItems.splice(idx,1);
      this.calcTotal();
    });
  },

  calcTotal(){
    var t=0;
    this.orderItems.forEach(i=>{t+=i.quantity*i.unitPrice;});
    this.curOrder.totalAmount=t.toFixed(2);
  },

  calcSubtotal(){
    this.newItem.subTotal=(this.newItem.quantity*this.newItem.product.price).toFixed(2);
  },

  showCreate(){
    this.orderItems=[];
    this.newItem={product:{id:null, name:'',price:0},quantity:1,unitPrice:0,subTotal:0};
    this.curOrder={id:null,supplier:{id:0, name:''},totalAmount:0,remark:''};
    this.barcodeInput='';
    this.showDialog=true;
    this.status=2;
  },
  
  showDetail(orderId){
    request({method:"GET",url:"/api/purchase/getOrder?id="+orderId},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK) return;
      this.curOrder=resp.data;
      this.status=resp.data.status;
      this.orderItems=resp.data.items||[];
      var dt = new Date();
      dt.setTime(this.curOrder.createAt);
      this.curOrder.createAt = datetime2str(dt);
      this.showDialog=true;
    });
  },

  onCancelOrder(){
    if(!this.curOrder.id) {
        this.showDialog=false;
        return;     
    }
    cancelOrder(this.curOrder.id, ()=>{
        this.$emit('orderCanceled');
        this.showDialog=false;
    }, (code, info)=>{
        this.$refs.errMsg.showErr(code, info);
    })
  },

  onConfirmOrder(){
    if(this.orderItems.length==0){
      this.$refs.errMsg.show(this.tags.pleaseAddProduct);
      return;
    }

    completeOrder(this.curOrder.id, ()=>{
        this.$emit('orderCompleted');
        this.showDialog=false;
    }, (code, info)=>{
        this.$refs.errMsg.showErr(code, info);
    })
  },
  
  onSupplierChanged(){
    if(!this.curOrder.id)return;
    var dta={id:this.curOrder.id,supplierId:this.curOrder.supplier.id,supplierName:this.curOrder.supplier.name};
    request({method:"PUT",url:"/api/purchase/setSupplier",data:dta},this.service.name).then(resp=>{
      if(resp.code!=RetCode.OK){
        this.$refs.errMsg.showErr(resp.code,resp.info)
        return;
      }
    });
  },
  onHide() {
    this.$emit('hide');
  }
},

template:`
<!-- 采购订单对话框 -->
<q-dialog v-model="showDialog" persistent maximized @hide="onHide">
  <q-card>
    <q-card-section class="row items-center q-pb-none">
      <div class="text-h6">{{status===2?tags.createOrder:tags.orderDetail}}</div>
      <q-space></q-space>
      <q-btn icon="close" flat round dense v-close-popup></q-btn>
    </q-card-section>
    <q-card-section>
      <!-- 扫码快速录入 -->
      <div class="row q-col-gutter-sm q-mb-md" v-if="status!=1">
        <div class="col-12">
          <q-btn color="primary" icon="qr_code_scanner" :label="tags.scanBarcode" @click="scanAndAdd" class="full-width" size="lg"></q-btn>
        </div>
      </div>

      <div class="text-subtitle2 q-mb-sm q-mt-md">{{tags.items}}</div>
      <q-separator></q-separator>
      <!-- 新增商品信息 -->
      <div class="row q-col-gutter-sm q-mt-sm" v-if="status!=1">
        <div class="col-4"><product-selector v-model="newItem.product" :serviceName="service.name" :label="tags.productName" dense @update:model-value="calcSubtotal"></product-selector></div>
        <div class="col-2"><q-input v-model.number="newItem.quantity" :label="tags.quantity" type="number" dense min="1" @update:model-value="calcSubtotal"></q-input></div>
        <div class="col-3"><q-input v-model.number="newItem.product.price" :label="tags.unitPrice" type="number" dense min="0" @update:model-value="calcSubtotal"></q-input></div>
        <div class="col-2"><q-input v-model.number="newItem.subTotal" :label="tags.subTotal" dense readonly></q-input></div>
        <div class="col-1 flex items-center justify-center">
          <q-btn color="primary" icon="add" @click="addItemToList"></q-btn>
        </div>
      </div>

      <!-- 已添加商品列表 -->
      <q-table v-if="orderItems.length>0" :rows="orderItems" :columns="[
        {name:'productName',label:tags.productName,field:'productName'},
        {name:'quantity',label:tags.quantity,field:'quantity'},
        {name:'unitPrice',label:tags.unitPrice,field:'unitPrice'},
        {name:'subTotal',label:tags.subTotal,field:'subTotal'},
        {name:'action',label:tags.operation,field:'action'}
      ]" row-key="index" flat dense hide-bottom>
        <template v-slot:body-cell-action="props">
          <q-td :props="props">
           <q-btn v-if="status!=1" flat dense color="negative" icon="delete" @click="doRemoveItem(props.rowIndex)"></q-btn>
          </q-td>
        </template>
      </q-table>
      <q-separator class="q-mt-md"></q-separator>
      <div class="text-subtitle2 q-mb-sm q-mt-md">{{tags.summary}}</div>
      <div v-if="status!=1">
        <supplier-selector v-model="curOrder.supplier" :serviceName="service.name" :label="tags.supplierName"
        @update:model-value="onSupplierChanged" dense></supplier-selector>
        <div><q-input v-model="curOrder.remark" :label="tags.remark" dense></q-input></div>
      </div>
      <div v-else>
       <div class="row q-col-gutter-sm q-mt-sm">
        <div class="col"><q-icon color="blue" size="1em" name="shopping_cart"></q-icon>{{tags.supplierName}}:{{curOrder.supplierName}}</div>
        <div class="col"><q-icon color="orange" size="1em" name="monetization_on"></q-icon>{{tags.totalAmount}}:{{curOrder.totalAmount}}</div>
       </div>
       <div>
        {{curOrder.remark}}<br>
        <div class="text-right">{{curOrder.creator}} @ {{curOrder.createAt}}<div>
       </div>
      </div>
    </q-card-section>
    <q-card-actions align="right" v-if="status!=1">
      <q-btn flat :label="tags.cancel" color="grey" @click="onCancelOrder"></q-btn>
      <q-btn unelevated :label="tags.completeOrder" color="primary" @click="onConfirmOrder"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog ref="errMsg"></component-alert-dialog>
`
}
