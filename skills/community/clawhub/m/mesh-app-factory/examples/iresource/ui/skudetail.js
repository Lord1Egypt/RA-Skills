import SupplierInput from "./components/supplier_selector.js";
export default {
inject:['service', 'tags'],
components:{
    "supplier-input":SupplierInput
},
data() {return {
    id:this.$route.query.id,
    skuInfo:{}, //sku信息
    ctrl:{fun:'',dta:{},skuTypes:[]},
    suppliers:[], //供应商
    feedbacks:[], //使用反馈
    edtSup:{show:false,supplier:'',price:''}
}},
created(){
    this.get();
    this.getSuppliers();
    this.getFeedbacks();
    for(var i in this.tags.skuType) {
        this.ctrl.skuTypes.push({label:this.tags.skuType[i],value:i});
    }
},
methods:{
get() {
    var url = "/api/sku/get?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var dt=new Date();
        dt.setTime(resp.data.createAt*60000);
        resp.data.createAt_s=date2str(dt);
        resp.data.type_s=this.tags.skuType[resp.data.type];
        this.skuInfo=resp.data;
    })
},
update() {
    var opts={method:"PUT",url:"/sku/update",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        copyObjTo(this.ctrl.dta, this.skuInfo);
        this.ctrl.fun='';
    });
},
remove() {
    var opts={method:"DELETE",url:"/sku/remove?id="+this.id};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.service.back();
    });
},
//反馈记录操作
getFeedbacks() {
    var url = "/api/sku/listFeedback?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.feedbacks=[];
            return;
        }
        var dt=new Date();
        for(var e of resp.data.list) {
            dt.setTime(e.createAt*60000);
            e.createAt_s=date2str(dt);
            e.level_s=this.tags.fbLevel[e.level];
        }
        this.feedbacks=resp.data.list;
    });
},
show_edit() {
    copyObjTo(this.skuInfo, this.ctrl.dta);
    this.ctrl.dta.id=this.id;
    this.ctrl.fun='edit';
},
//供应商操作
getSuppliers() {
    var url = "/api/sku/listSupplier?id="+this.id;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.suppliers=[];
            return;
        }
        var dt=new Date();
        for(var e of resp.data.list) {
            dt.setTime(e.createAt*60000);
            e.createAt_s=date2str(dt);
        }
        this.suppliers=resp.data.list;
    });
},
showAddSup() {
    this.edtSup.supplier='';
    this.edtSup.price='';
    this.edtSup.show=true;
},
addSupplier() {
    var url = "/api/sku/addSupplier";
    var dta={id:this.id,supplier:this.edtSup.supplier.id,price:this.edtSup.price};
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        dta.createAt_s=date2str(new Date());
        dta.name=this.edtSup.supplier.name;
        this.suppliers.push(dta);
        this.edtSup.show=false;
    });
},
rmvSupplier(i) {
    var url = "/api/sku/removeSupplier?id="+this.id
        +"&supplier="+this.suppliers[i].supplier;
    request({method:"DELETE",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.suppliers.splice(i,1);
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.detail}}-{{skuInfo.name}}</q-toolbar-title>
    <q-btn icon="delete_forever" @click="remove" flat dense></q-btn>
    <q-btn icon="edit" @click="show_edit" flat dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div v-if="ctrl.fun==''">
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.name}}</q-item-section>
   <q-item-section>{{skuInfo.name}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.type}}</q-item-section>
   <q-item-section>{{skuInfo.type_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.noHead}}</q-item-section>
   <q-item-section>{{skuInfo.noHead}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.monthDepr}}</q-item-section>
   <q-item-section>{{skuInfo.monthDepr}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.yearDepr}}</q-item-section>
   <q-item-section>{{skuInfo.yearDepr}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.speci}}</q-item-section>
   <q-item-section>{{skuInfo.speci}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section>{{skuInfo.cmt}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.createAt}}</q-item-section>
   <q-item-section>{{skuInfo.createAt_s}}</q-item-section>
  </q-item>
 </q-list>
</div>
<div v-else>
 <q-list dense>
  <q-item>
   <q-item-section>{{tags.name}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.name" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.type}}</q-item-section>
   <q-item-section><q-select v-model="ctrl.dta.type" :options="ctrl.skuTypes" emit-value map-options></q-select></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.noHead}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.noHead" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.monthDepr}}</q-item-section>
   <q-item-section><q-input v-model.number="ctrl.dta.monthDepr" dense type="number"></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.yearDepr}}</q-item-section>
   <q-item-section><q-input v-model.number="ctrl.dta.yearDepr" dense type="number"></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.sku.speci}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.speci" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section><q-input v-model="ctrl.dta.cmt" dense></q-input></q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.createAt}}</q-item-section>
   <q-item-section>{{skuInfo.createAt_s}}</q-item-section>
  </q-item>
 </q-list>
 <div class="text-right">
  <q-btn flat :label="tags.cancel" color="primary" @click="ctrl.fun=''"></q-btn>
  <q-btn icon="done" :label="tags.ok" color="primary" @click="update"></q-btn>
 </div>
</div>
<q-separator inset></q-separator>
<q-banner inline-actions class="bg-indigo-1 q-ma-sm" dense>
  {{tags.supplier.title}}
  <template v-slot:action>
   <q-icon flat color="primary" name="add_circle" @click.stop="showAddSup"></q-icon>
  </template>
</q-banner>
<q-list dense>
  <q-item v-for="(s,i) in suppliers">
   <q-item-section>{{s.name}}</q-item-section>
   <q-item-section>{{s.price}}</q-item-section>
   <q-item-section side>
    <q-btn icon="cancel" color="red" @click="rmvSupplier(i)" flat></q-btn>
   </q-item-section>
  </q-item>
  <q-item v-show="edtSup.show">
   <q-item-section>
    <supplier-input v-model="edtSup.supplier" :label="tags.supplier.title"></supplier-input>
   </q-item-section>
   <q-item-section>
    <q-input v-model.number="edtSup.price" :label="tags.sku.price" dense type="number"></q-input>
   </q-item-section>
   <q-item-section side>
   <q-btn :label="tags.ok" color="primary" @click="addSupplier" flat></q-btn>
    <q-btn :label="tags.cancel" color="primary" @click="edtSup.show=false" flat></q-btn>
   </q-item-section>
  </q-item>
</q-list>

<q-banner inline-actions class="bg-indigo-1 q-ma-sm" dense>
  {{tags.sku.feedback}}
</q-banner>
<q-list dense>
  <q-item v-for="f in feedbacks">
   <q-item-section>{{f.level_s}}</q-item-section>
   <q-item-section>{{f.creator}}</q-item-section>
   <q-item-section side>{{f.createAt_s}}</q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}